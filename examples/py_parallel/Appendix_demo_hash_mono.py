#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 10:24:30 2021

@author: wangjianxiong


说明：
       1. 哈希分组结果的均匀程度，取决于作为哈希运算依据的变量取值的分布！！！！只要变量取值足够分散，就能保证哈希分组均匀！
       2. 这就意味着：要么找到取值分散的变量，要么需要先在数据表中生成一个随机列，而后再基于该列进行哈希分组。
       
       3. 需不需要先对一个大数取余，这个需要详细查看里面的机制！！！目前不详，只是在有些情况下，先对大数取余，效果较好！！！！（也不知道为什么）

"""


import pandas as pd
from   pandas import DataFrame

import gc   # garbage collector

import time


import random



import psycopg2     # 该库用于在 python 中调用 postgreSQL

from  multiprocessing import Pool      # 用于控制并行执行的包



# 添加python搜索路径， 后续搜索导入的库包时，就会从该路径导入
# path = "/Users/wangjianxiong/Desktop/《并行大数据处理：基于Python、PostgreSQL及其他》/1_书稿_ing/2_各章图表、示例代码及附加资料/CH09_分布式并行处理/2_代码/"
path = f"/Users/afirez/studio/python/auto-trade/examples/py_parallel/"
import sys
sys.path.append(path)


import parallel_process_postgres as ppp   # 导入该模块，该模块专为分析裁判文书而写。





#####################
# 0. 准备工作



#    0.1 创建数据库连接

#  创建数据库 股票分析数据库 的连接 
conn, curs, engine = ppp.creat_conn_with_pg(dbname='stock_data_csmar')





#####################
# 1. 演示


# 获取数据
df = pd.read_sql_query("""SELECT 证券代码,
                                 交易日期,
                                 开盘价,
                                 流通市值
                                           
                                            FROM     a_1_个股日度数据表_csmar
                                            LIMIT(100000);""", 
                        engine)





# 进行hash运算

process_num = 3
# 给出需要导入数据的“日期”：根据哈希运算结果，取一个

hash_var = '交易日期'
df['hash_num']    = df[hash_var].apply(hash)                       # 原理：先做哈希运算，再通过取余数分组，并将“余数等于子进程编号相同”的组留下）
df['process_num'] = df['hash_num'].apply(lambda x: x%100000)
df['process_num'] = df['process_num'].apply(lambda x: x%process_num)        # 先对一个大数求余，再继续求余，就能获得一个均衡的结果！


# 查看取值分布
df['process_num'].value_counts()



