import time
import datetime

import numpy as np

import akshare as ak

import stock_config as scg
import stock_constant as sct
import stock_db as sdb


def stock_code_net_to_csv():
    """
    获取A股股票代码，并保存到data/xxx.csv文件中
    新浪日行情数据需要：沪交所股票代码，代码添加前缀sh，深交所股票代码，代码添加前缀sz
    :return: [上交所DataFrame,深交所DataFrame]
    """
    stock_sh_a_spot_em_df = ak.stock_sh_a_spot_em()
    # 修改股票代码前缀
    stock_sh_a_spot_em_df['代码'] = \
        stock_sh_a_spot_em_df['代码'].apply(lambda _: str(_))
    # stock_sh_a_spot_em_df['代码'].apply(lambda x: "{}{}".format('sh', x))
    # 保存
    stock_sh_a_spot_em_df.to_csv(sct.sh_code_path)

    stock_sz_a_spot_em_df = ak.stock_sz_a_spot_em()
    # 修改股票代码前缀
    stock_sz_a_spot_em_df['代码'] = \
        stock_sz_a_spot_em_df['代码'].apply(lambda _: str(_))
    # stock_sz_a_spot_em_df['代码'].apply(lambda x: "{}{}".format('sz', x))
    # 保存
    stock_sz_a_spot_em_df.to_csv(sct.sz_code_path)
    return stock_sh_a_spot_em_df, stock_sz_a_spot_em_df


def start():
    """
    量化投资程序入口
    :return:
    """
    config_df = scg.read_config()
    # 如果配置是空，则获取沪深A股信息，获取code，保存到配置
    if config_df.empty:
        sh_df, sz_df = stock_code_net_to_csv()
        # 补全本地配置信息
        for index, row in sh_df.iterrows():
            config_df.loc[len(config_df), config_df.columns] = (row['代码'], row['名称'], sct.start_date, 0)
        for index, row in sz_df.iterrows():
            config_df.loc[len(config_df), config_df.columns] = (row['代码'], row['名称'], sct.start_date, 0)
        # 保存到本地
        scg.save_config(config_df)
        print('初始化配置信息，并保存到本地成功...')
    else:
        print('已经初始化过本地配置...')
    # 开始更新日行情数据
    update_stock_zh_a_daily_eastmoney()


def update_stock_zh_a_daily_eastmoney():
    """
    东方财富日行情数据，沪深A股，先从本地配置获取股票代码，再获取日行情数据
    获取成功或失败，记录到本地数据，以便股票数据更新完整
    :return:
    """
    success_code_list = []
    except_code_list = []
    empty_data_code_list = []
    # 读取配置信息
    config_df = scg.read_config()
    # config_df["daily_update_time"] = config_df["daily_update_time"].apply(lambda x: x - 1 if x == 20230209 else x)
    if config_df.empty:
        print('配置信息错误，请检查...')
        return
    
    end_time = time.strftime('%Y%m%d', time.localtime())
    if type(config_df['daily_update_time'][0]) is np.int64 :
        end_time = np.int64(end_time)

    config_df_ = config_df[config_df['daily_update_time'] < end_time]
    print(f'需要更新 {len(config_df_)} 个')
    print(config_df_)

    if config_df_.empty:
        # 需要更新的数据
        print('已更新到最新')
        return
    
    # return

    for index, row in config_df_.iterrows():
        code = row['code']
        start_time = row['daily_update_time']

        if start_time == end_time:
            # 该 code 数据已更新
            print('成功获取股票: index->{} {}日行情数据'.format(index, code), ' 开始时间: {} 结束时间: {}'.format(start_time, end_time))
            continue

        if str(start_time) != str(sct.start_date):
            start_time =  datetime.datetime.strptime(f'{start_time}','%Y%m%d') + datetime.timedelta(days=1)
            start_time = datetime.datetime.strftime(start_time, '%Y%m%d')

        try:
            except_code = str(code)
            df = ak.stock_zh_a_hist(
                symbol=str(code),
                start_date=start_time,
                end_date=end_time,
                adjust="qfq")
        except:
            except_code_list.append(except_code)
            # 更新配置信息config_df
            config_df.loc[config_df['code'] == code, 'error_daily_update_count'] \
                = row['error_daily_update_count'] + 1

            print("发生异常code ", except_code)
            continue

        print('成功获取股票: index->{} {}日行情数据'.format(index, code), ' 开始时间: {} 结束时间: {}'.format(start_time, end_time))
        if df.empty:
            # 更新配置信息config_df
            # config_df.loc[config_df['code'] == code, 'daily_update_time'] = end_time
            # config_df.loc[config_df['code'] == code, 'error_daily_update_count'] = 0
            empty_data_code_list.append(code)
            continue

        # 获取对应的子列集
        sub_df = df[['日期', '开盘', '最高', '最低', '收盘', '成交量', '成交额']]
        # net_df 的列名可能和数据库列名不一样，修改列名对应数据库的列名
        sub_df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount']
        # 修改 index 为 date 去掉默认的 index 便于直接插入数据库
        sub_df.set_index(['date'], inplace=True)
        sub_df.insert(sub_df.shape[1], 'code', str(code))
        sdb.to_table(sub_df, "stock_daily_price")
        # 更新配置信息config_df
        config_df.loc[config_df['code'] == code, 'daily_update_time'] = end_time
        config_df.loc[config_df['code'] == code, 'error_daily_update_count'] = 0
        # 间隔更新到本地配置
        if index % 100 == 0:
            scg.save_config(config_df)
            print('index: {} 更新本地配置一次...'.format(index))

        success_code_list.append(code)
        print(sub_df)
    # 同步配置到本地
    scg.save_config(config_df)

    print('更新本地配置成功...')
    print("成功请求的code： ", success_code_list)
    print("错误请求code： ", except_code_list)
    print("空数据请求code： ", empty_data_code_list)


if __name__ == '__main__':
    # df = sdb.delete_daily_duplicated(date='2023-02-09')
    # print(df)

    # df = sdb.stock_daily(code='000002', start_time='2023-02-08', end_time='2023-02-09')
    # print(df)

    # df = sdb.all_stock_daily(start_time='2023-02-09', end_time='2023-02-09')
    # print(df)
    
    start()

    pass
