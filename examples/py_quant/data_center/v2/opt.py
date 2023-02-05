import asyncio
import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait
import multiprocessing

import akshare as ak
import pandas as pd

import stock_constant as sc
import stock_db as sdb

"""
优化股票日行情数据请求速度

也没啥好说的，就是把日行情请求抽成任务函数，然后扔到进程池里面执行即可，

这里要说下进程间内存并不共享，那么如何保存每个请求的结果呢？

需要用 multiprocessing.Manager() 来构建对象，即进程可以共享这些对象。

核心代码如下，结果 5k 个股票请求时间 20150101 - 20221202 时间段，

全部请求完毕并保存到数据库，大概 6 分钟左右。用多进程效果也是一致的，注释的代码就是使用多进程的。


要点分析：
进程间数据共享要通过这样子来创建，这里创建了两个列表，还有其他支持的数据类型，具体的自己查看 api.

with multiprocessing.Manager() as MG:
    success_code_list = MG.list()
    except_code_list = MG.list()
"""

def _update_daily_task(self, code, start_time,
                       end_time, except_code_list,
                       index, success_code_list):
    try:
        df = ak.stock_zh_a_hist(
            symbol=str(code),
            start_date=start_time,
            end_date=end_time,
            adjust="qfq")
    except:
        except_code_list.append(code)
        print("发生异常code ", code)
        return

    print('成功获取股票: index->{} {}日行情数据'.format(index, code)
          , ' 开始时间: {} 结束时间: {}'.format(start_time, end_time),
          f'数据是否为空：{df.empty}')
    if df.empty:
        success_code_list.append(code)
        return

        # 获取对应的子列集
    sub_df = df[['日期', '开盘', '最高', '最低', '收盘', '成交量', '成交额']]
    # net_df 的列名可能和数据库列名不一样，修改列名对应数据库的列名
    sub_df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount']
    # 修改 index 为 date 去掉默认的 index 便于直接插入数据库
    sub_df.set_index(['date'], inplace=True)
    sub_df.insert(sub_df.shape[1], 'code', str(code))
    sdb.to_table(sub_df, "stock_daily_price")
    success_code_list.append(code)
    # print(sub_df)

async def update_daily_multi_io(self):
    """
    更新股票日行情数据
    东方财富日行情数据，沪深A股，先从本地配置获取股票代码，再获取日行情数据
    获取成功或失败，记录到本地数据，以便股票数据更新完整
    :return:
    """
    last_time = time.time()
    with multiprocessing.Manager() as MG:
        success_code_list = MG.list()
        except_code_list = MG.list()
        # 读取配置信息
        config_df = self.config.config_df
        if config_df.empty:
            print('配置信息错误，请检查...')
            return

        end_time = self.config.update_end_time()
        executor = ProcessPoolExecutor()
        futures = []
        loop = asyncio.get_event_loop()
        for index, row in config_df.iterrows():
            code = row['code']
            start_time = self.config.daily_start_time(code)

            if start_time == end_time:
                # 已经更新过了
                continue
            future = loop.run_in_executor(executor, self._update_daily_task,
                                          code, start_time,
                                          end_time, except_code_list,
                                          index, success_code_list)
            # future = executor.submit(self._update_daily_task,
            #                          code, start_time,
            #                          end_time, except_code_list,
            #                          index, success_code_list)
            futures.append(future)
        # wait(futures)
        if len(futures) > 0:
            await asyncio.wait(futures)

        # 更新配置信息
        for code in success_code_list:
            # 更新配置信息config_df
            config_df.loc[config_df['code'] == code, 'daily_update_time'] = end_time
            config_df.loc[config_df['code'] == code, 'error_daily_update_count'] = 0
        for code in except_code_list:
            # 更新配置信息config_df
            config_df.loc[config_df['code'] == code, 'error_daily_update_count'] \
                = row['error_daily_update_count'] + 1

        # 同步配置到本地
        self.config.save_config()
        # 手动触发去重
        sdb.optimize('stock_daily_price')

        print('更新本地配置成功...')
        print("成功请求的code： ", success_code_list)
        print("错误请求code： ", except_code_list)
        print(f'日行情更新耗时: {time.time() - last_time}')


"""
优化个股常用指标计算速度
计算的指标

指标计算是 cpu 任务密集型，所以用进程池。

本体系建立了一个指标表，这个表只记录个股自身相关的指标，
分别是个股自身振幅百分比 amp 以及均线指标 ma，这两个指标包含 5、10、20、50、120、250 日的指标。

分拆任务

根据硬件自身条件 cpu 核数来启动进程池，拆分股票计算池，并分配到不同的进程，计算完毕后把指标更新到数据库。

表结构：

columns = {
        'date': 'Date',
        'code': 'String',
        'amp5': 'Float32',
        'amp10': 'Float32',
        'amp20': 'Float32',
        'amp50': 'Float32',
        'amp120': 'Float32',
        'amp250': 'Float32',
        'ma5': 'Float32',
        'ma10': 'Float32',
        'ma20': 'Float32',
        'ma50': 'Float32',
        'ma120': 'Float32',
        'ma250': 'Float32'
    }

要点分析：
update_common_ind() 函数是全部股票根据 cpu 核数划分任务池。
_update_common_ind_task() 是任务函数，每个进程领取的部分股票池计算。
"""
def _update_common_ind_task(self, codes, start_time, end_time, success_list):
    """
    计算个股自身的的指标，股票池的形式查股票数据
    :param codes: 任务集合的股票池
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param success_list: 计算成功列表
    :return:
    """

    # 查询基本日行情数据
    stocks_df = sdb.pool_stock_daily(codes, start_time, end_time, ['close'])
    if stocks_df.empty:
        return

    # 计算完的列表，用于后续拼接一次性插入数据库
    ind_df_list = []
    for code in codes:
        daily_df = stocks_df.loc[stocks_df['code'] == code]
        # 个股自身的振幅
        ind_df = mathutils.amplitude(daily_df['close'], amp5=5, amp10=10,
                                     amp20=20, amp50=50, amp120=120, amp250=250)
        # 计算个股ma
        ema_list = [5, 10, 20, 50, 120, 250]
        for i in ema_list:
            key = f'ma{str(i)}'
            ind_df[key] = ta.EMA(daily_df['close'], timeperiod=i)

        # 更新到指标表
        if not ind_df.empty:
            ind_df['code'] = code
            ind_df_list.append(ind_df)
            success_list.append(code)
        # print(f'{code} 指标计算完毕')
    result = pd.concat(ind_df_list)
    if not result.empty:
        sdb.to_indicator_table(result)
    print(f'该任务完毕，插入数据库条目数: {len(result)}')

    # 释放
    del stocks_df
    del ind_df_list

def update_common_ind(self):
    """
    更新常用指标
    :return:
    """
    # 更新常用指标
    config = self.config
    config_df = config.config_df
    format_str = '%Y-%m-%d'
    end_time = config.update_end_time()
    last_time = time.time()
    # 先去重，避免更新有冲突
    sdb.optimize(sdb.STOCK_DAILY_TABLE)
    sdb.optimize(sdb.STOCK_INDICATOR_TABLE)

    # 根据 cpu 个数拆分股票任务数
    cpu_count = os.cpu_count()
    with multiprocessing.Manager() as mg:
        # 进程内数据共享
        success_list = mg.list()
        all_codes = list(config_df['code'])
        item_count = int(len(all_codes) / cpu_count)
        print(f'每个任务计算指标个数：{item_count} codeLength: {len(all_codes)}')
        pool = multiprocessing.Pool(processes=cpu_count)
        for index in range(cpu_count):
            start_index = index * item_count
            end_index = start_index + item_count
            # 如果是最后一个任务，索引到最后
            if index == cpu_count - 1:
                end_index = len(all_codes)
            # 切片，分任务
            part_codes = all_codes[start_index: end_index]
            ind_start_time = config.ind_start_time(part_codes[0])
            # 偏移最大计算日期，最大日期 250 日均线，所以日行情数据开始位置要往前偏移
            start_time = timeutils.time_str_delta(ind_start_time, format_str, days=-365)
            if ind_start_time == end_time:
                print(f'已经计算过 时间:{end_time}')
                continue

            print(f'任务{index} 开始位置：{start_index} 结束位置：{end_index}')
            # 异步启动任务
            pool.apply_async(self._update_common_ind_task,
                             args=(part_codes, start_time, end_time, success_list))
        # 等待所有任务完毕
        pool.close()
        pool.join()
        print(f'指标计算完毕,耗时：{time.time() - last_time}')
        print(f'指标计算完毕 成功股票个数：{len(success_list)}')

        # 更新配置信息
        for code in success_list:
            config_df.loc[config_df['code'] == code, 'ind_update_time'] = end_time

    # 同步配置到本地
    self.config.save_config()
    # 操作完毕触发去重
    sdb.optimize(sdb.STOCK_INDICATOR_TABLE)