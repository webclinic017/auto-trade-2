#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 10:58:29 2021

@author: wangjianxiong
"""


import pandas as pd


import time









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
conn, curs, engine = ppp.creat_conn_with_pg(dbname = 'stock_data_for_test')

#  创建数据库 stock_data 的连接 
conn2, curs2, engine2 = ppp.creat_conn_with_pg(dbname = 'stock_data')




#    0.2 给出并行执行进程数

parallel_procedure_number = 4



#    0.3 给出当前日期

time_local           = time.localtime()       # 提取本地时间
date_of_today        = time.strftime("%Y-%m-%d", time_local)   # 转为表示日期的字符串



#####################
# 1. 查询并行计算进度


while True:
    
    
    
    #    1.1 查询进度信息
    
    time.sleep(2)   # 给出查询间隔
    
    try:
        df1  = pd.read_sql_query("""SELECT   count(*)
                                               FROM parallel_tool_并行任务分配信息表 
                                                WHERE 处理状态  = 0          --  未被处理
                                                      ;""",    
                                 con    = engine)  # 读取数据
        
        
        df2  = pd.read_sql_query("""SELECT   count(*)
                                               FROM parallel_tool_并行任务分配信息表 
                                                WHERE 处理状态  = 1          --  处理中
                                                      ;""",    
                                 con    = engine)  # 读取数据
        
        
        # 全部小组处理完毕，监测进程退出
        if df1['count'][0] == 0:
            print('全部分组计算完毕！！！')
            break
        
        
    except:
        print('全部分组计算完毕！！！')
        break
        
        
    #    1.2 给出当前日期、时间信息
    time_local    = time.localtime()       # 提取本地时间
    date_now      = time.strftime("%Y-%m-%d", time_local)   # 转为表示日期的字符串
    time_now      = time.strftime("%H时%M分", time_local)   # 转为表示小时和分钟的字符串

    
    
    #    1.3 展示进度信息
    print('单机版并行计算进度监测：现在是{} - {} ，已完成 {} 组， 有 {} 组待进行计算'.format(date_now, time_now, df2['count'][0], df1['count'][0]))
    

