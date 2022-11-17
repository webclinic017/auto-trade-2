#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
并行下载股票 （京沪深 A 股）
"""

from mimetypes import suffix_map
import pandas as pd
from   pandas import DataFrame

import gc   # garbage collector

import time

import psycopg2     # 该库用于在 python 中调用 postgreSQL

from  multiprocessing import Pool  

# 添加python搜索路径， 后续搜索导入的库包时，就会从该路径导入
# path = "/Users/wangjianxiong/Desktop/《并行大数据处理：基于Python、PostgreSQL及其他》/1_书稿_ing/2_各章图表、示例代码及附加资料/CH09_分布式并行处理/2_代码/"
path = f"/Users/afirez/studio/python/auto-trade/examples/py_quant/common/"
import sys
sys.path.append(path)

import config

print(config.db_pg)

import common_pg

import akshare as ak

# 0 准备工作

dbname = "k_house"
#   0.1 创建数据库连接

#  创建数据库 股票分析数据库 的连接 
# conn, curs, engine = common_pg.creat_conn_with_pg(dbname=f'{dbname}_for_test')

#  创建数据库 stock_data 的连接 
conn2, curs2, engine2 = common_pg.creat_conn_with_pg(dbname=dbname)

#  0.2 给出并行执行进程数
worker_number = 4

#  0.3 给出当前日期

time_local           = time.localtime()       # 提取本地时间
date_of_today        = time.strftime("%Y-%m-%d", time_local) 

start_date_v1 = "20000101"

end_date_v1 = "20220729"

start_date_list = [
    start_date_v1,
    "20220730",
]

end_date_list = [
    end_date_v1,
    "20221023",
]

start_date = "20220730"
end_date = "20221023"

# 1. 在数据库中创建数据表 a_k_dayly股票日k行情表 

def create_db_table_k_dayly():
    """
    暂时不用
    """
    try:
        #   1.1 为了避免出现已存在错误，先删除
        curs2.execute("""DROP TABLE a_k_dayly_股票日k行情表;""")
        conn2.commit()
    except:
        conn2.rollback()
    
    try:
        #   1.2 建数日度股票交易情况统计表
        curs2.execute("""CREATE TABLE a_k_dayly_股票日k行情表
                           (date_交易日期           date           NOT NULL,
                            
                            symbel_代码            numeric(20,0)  DEFAULT -1,
                            name_名称              numeric(20,0)  DEFAULT -1,
                            open_开盘              numeric(20,0)  DEFAULT -1,
                            close_收盘             numeric(20,0)  DEFAULT -1,
                            low_最低               numeric(20,0)  DEFAULT -1,
                            high_最高              numeric(20,0)  DEFAULT -1,
                            volume_成交量          numeric(20,0)  DEFAULT -1,
                            );""")

        #   1.3 添加索引
        curs2.execute("""CREATE INDEX a_k_dayly_date_交易日期 ON a_k_dayly_股票日k行情表 (date_交易日期);"""
                 )
                            
        conn2.commit()
    
        print('a_k_dayly_股票日k行情表 创建成功')
    
    except Exception as e:
        print(e)
        conn2.rollback()
        print('a_k_dayly_股票日k行情表 创建失败')

# 2. 在数据库中创建数据表 a_symbel_股票代码表 
def create_db_table_symbel():
    """
    暂时不用
    """
    try:
        #   2.1 为了避免出现已存在错误，先删除
        curs2.execute("""DROP TABLE a_symbel_股票代码表;""")
        conn2.commit()
    except:
        conn2.rollback()
    
    try:
        #   2.2 建数日度股票交易情况统计表
        curs2.execute("""CREATE TABLE a_symbel_股票代码表
                           (date_上市日期         date           NOT NULL,
                            
                            symbel_代码            numeric(20,0)  DEFAULT -1,
                            name_名称              numeric(20,0)  DEFAULT -1,
                            );""")

        #   3.3 添加索引
        curs2.execute("""CREATE INDEX a_symbel_symbel_代码 ON a_symbel_股票代码表 (symbel_代码);"""
                 )
                            
        conn2.commit()
    
        print('a_symbel_股票代码表 创建成功')
    
    except Exception as e:
        print(e)
        conn2.rollback()
        print('a_symbel_股票代码表 创建失败')

#  3 在数据库中创建任务分配表，用于存储分组信息及分组处理进度信息

#    3.1 创建 task_tool_并行任务分配信息表    

def stock_info_code_name_prepare():
    df = ak.stock_info_a_code_name()
    table_name_stock_info_a_code_name = 'stock_info_a_code_name'
    df.to_sql(table_name_stock_info_a_code_name,
          engine2,
          index     = False,
          if_exists = 'replace')    # 写入数据库  还有一个参数是  append，那是附加在表后
    
    # 添加索引
    # curs2.execute(
    #     """
    #     CREATE  INDEX stock_info_a_code_name_code  ON  stock_info_a_code_name  (code); 
    #     """
    # )
    # conn2.commit()

    return df

def get_stock_info_code_name():
    df = pd.read_sql_query(f"""SELECT *
                                   FROM stock_info_a_code_name;""",
                        con = engine2)
    return df

def fetch_stock_zh_a_hist_to_db(symbol, period="daily", start_date=start_date, end_date=end_date, adjust=""):
    # ak.stock_zh_a_hist 可以在里面给 request 加入 timeout 参数
    hist_df = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust)
    table_name = f'stock_a_history_{period}_{symbol}'
    hist_df["code"] = symbol
    hist_df.to_sql(table_name,
          engine2,
          index     = False, # 布尔值，默认为True，将DataFrame索引写为列。使用index_label作为表中的列名。
        #   index_label=  "time",
        #   if_exists = 'replace', # 在插入新值之前删除表
          if_exists = 'append', # 将新值插入现有表。
    )    # 写入数据库  还有一个参数是  append，那是附加在表后
    
    #添加索引
    try:
        curs2.execute(
           f"""
            CREATE  INDEX {table_name}_code  ON  {table_name}  (code); 
            CREATE  INDEX {table_name}_日期  ON  {table_name}  (日期); 
            """
        )
        conn2.commit()
    except Exception as e:
        print(e)
        conn2.rollback()

def get_stock_zh_a_hist(symbol, period="daily", start_date=start_date, end_date=end_date, adjust=""):
    df = pd.read_sql_query(f"""SELECT *
                                   FROM stock_a_history_{period}_{symbol};""",
                        con = engine2)
    return df

def task_mgr_prepare(): 
    # 读入股票代码表
    df = get_stock_info_code_name()

    # 仅保留所需变量
    df = df[['code',]]
    df['task_tag'] = df['code']
    df = df[['task_tag',]]

    # 添加序号列： 后面将基于“序号列”的取值，来分配并行计算任务
    df['分组序号'] = [i for i in range(len(df))]             # 利用列表解析，生成连续编码的列表，并将其写入新建的数据列“分组序号”

    # 增加处理状态标记变量
    df['处理状态'] = 0
    return df

#    3.2 任务分配信息写入数据库   

def task_mgr_to_db(df):
    df.to_sql('task_tool_并行任务分配信息表',
          engine2,
          index     = False,
          if_exists = 'replace')    # 写入数据库  还有一个参数是  append，那是附加在表后
    # 添加索引
    try:
        curs2.execute("""CREATE  INDEX task_tool_1      ON  task_tool_并行任务分配信息表  (task_tag); 
                CREATE  INDEX task_tool_2      ON  task_tool_并行任务分配信息表  (分组序号);
                CREATE  INDEX task_tool_3      ON  task_tool_并行任务分配信息表  (处理状态);"""
            )
        conn2.commit()
    except Exception as e:
        print(e)
        conn2.rollback()

# 4. 基于“分组”，进行并行计算
#    4.0 准备工作：清空分组处理记录，以便重新开始
    # 如果首次执行，则执行以下操作：将所有处理记录归零
    # 如果是中断后执行，无需执行任何特别操作！！！
def task_tool_reset_state():
    try:
        curs2.execute("""UPDATE  task_tool_并行任务分配信息表
                   SET     处理状态     = %s;""", 
               (0,
                ))
        conn2.commit()
    except Exception as e:
        print(e)
        conn2.rollback()

def doOnStart():
    trycnt = 3  # max try cnt
    while trycnt > 0:
        try:
            code_df = stock_info_code_name_prepare()
            task_df = task_mgr_prepare()
            # task_tool_reset_state()
            task_mgr_to_db(task_df)
            trycnt = 0 # success
        except Exception as ex:
           if trycnt <= 0: print("Failed to doOnStart: " + "\n" + str(ex))  # done retrying
           else: trycnt -= 1  # retry
           time.sleep(0.5)  # wait 1/2 second then retry


def doOnTask(task_tag):
    symbol = task_tag
    fetch_stock_zh_a_hist_to_db(symbol=symbol)


#    2.1 创建并行执行函数
def task_run(i, worker_num):
    """
    目标：
         本函数为并行任务函数，用于在多进程环境中进行并行数据处理；
         
    参数：
         i,             int,     执行本函数的当前进程的编号，从0开始编号；
         worker_num,   int,     执行并行计算的并行进程总数。
    
    返回值：
          None

    """

    print(f"分组{i} start")

        #  创建数据库 股票分析数据库 的连接 
    # conn, curs, engine = common_pg.creat_conn_with_pg(dbname=f'{dbname}_for_test')
    
    #  创建数据库 stock_data 的连接 
    conn2, curs2, engine2 = common_pg.creat_conn_with_pg(dbname=dbname)
    
    
    count_bat = 0

    while True:

        ##########################
        #   2.1.0 设定退出条件：如果所有分组数据都被处理，则退出
        
        # 读入所有未处理的小组
        df  = pd.read_sql_query("""SELECT   *
                                              FROM task_tool_并行任务分配信息表 
                                                WHERE 处理状态  = 0          --  未被处理
                                                --LIMIT(1000)               -- 不能仅仅取一部分，应该全部都要取出来，不然会出错！！！（因为每次取到的，是同一批？）
                                                ;""",    
                                 con    = engine2)  # 读取数据
        
        print(f"{i} 未处理 {len(df)}")
        # 过滤出“被最大并行进程数整除后的余数”与“本进程编号相等”的数据行
        df['余数'] = df['分组序号']% worker_num

        print(f"{i} 余数 {df['余数']}")
        df = df[df['余数'] ==  i]
        
        print(f"{i} 余数 == i {df}")
        
        # 重设索引为依次渐增的数字索引       
        df.reset_index(drop=True,inplace=True) 
                
        
        # 如果满足条件的小组不存在，则跳出循环：此时，已经处理完毕
        if len(df) == 0:
            # conn.close()         # 断了数据库连接
            conn2.close()         # 断了数据库连接
            break

        ##########################
        #   2.1.1 导入待处理数据          
        
        #      2.1.1.0 准备阶段
        
        # 提取第一行所对应分组，作为待处理数据
        task_tag = df.at[0, 'task_tag'] 
        print(f"{i} task_tag {task_tag}")

        doOnTask(task_tag)

        curs2.execute("""UPDATE      task_tool_并行任务分配信息表
                            SET     处理状态              = %s   
                            WHERE   task_tag              = %s;""", 
                       (1,                                   # 用 1 表示该小组已经处理完毕
                        task_tag,
                        ))
        conn2.commit()

        # 累计并显示进度        
        count_bat += 1  
        if count_bat%1 == 0:
            print('代码文件 1_1_单机版_分布式并行计算方案_*.py 的第2步-->>> 第 {} 个子进程工作进度：已完成第 {} 组的数据处理，还有 {} 组数据等待处理 '.format(i, count_bat, len(df)))
 
    
        del df  # 手动删对象
        
        # 清理内存
        if count_bat%10 == 0:
            gc.collect()
            
    return None

#    2.2 调用并行执行函数         (MacOS上的新版 Spyder，并行也只能在“__name__ == '__main__'”在进行了？)

if __name__ == '__main__':

    doOnStart()
                
    t_start=time.time()
    pool = Pool(worker_number) # parallel_procedure_number 给出了并行执行的进程数
    
    for i in range(worker_number):
        time.sleep(3)    # 缺省值设成了 0.1，实际运行设高一点，以免各个进程在查询数据库时相互竞争...
        print('提醒：正在开启第 {} 个并行子进程'.format(i))
        pool.apply_async(task_run, (i, worker_number))
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    
    # 给出当前日期、时间信息
    time_local    = time.localtime()       # 提取本地时间
    date_now      = time.strftime("%Y-%m-%d", time_local)   # 转为表示日期的字符串
    time_now      = time.strftime("%H时%M分", time_local)   # 转为表示小时和分钟的字符串
    print('现在是 {} ，本次数据处理已执行完毕'.format(time_now))    
        
    #######################################        
            
    # Final. 做最后处理，并断开主进程的数据库连接
    
    # 删除任务分配表        
    curs2.execute("""
                    DROP  table  task_tool_并行任务分配信息表;
                    """)   
    conn2.commit()   
    
    # 断开主进程的数据库连接
    # conn.close()
    conn2.close()