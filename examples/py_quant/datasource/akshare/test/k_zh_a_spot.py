#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import akshare as ak
import pandas as pd
import sys
sys.path.append('/Users/afirez/studio/python/auto-trade/examples/py_quant/common')
sys.path.append('/Users/afirez/studio/python/auto-trade/examples/py_quant/common/common_pg.py')

# print("sys.path:",sys.path)
# import common_pg as common_db

print(ak.__version__)

# 实时行情数据
# 接口: stock_zh_a_spot
# 目标地址: http://vip.stock.finance.sina.com.cn/mkt/#hs_a
# 描述: A 股数据是从新浪财经获取的数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
# 限量: 单次返回所有 A 股上市公司的实时行情数据

stock_zh_a_spot_df = ak.stock_zh_a_spot()
print(stock_zh_a_spot_df)

# 0. 准备工作

dbname = "k_house"
#   0.1 创建数据库连接

#  创建数据库 股票分析数据库 的连接 
# conn, curs, engine = common_db.creat_conn_with_pg(dbname=f'{dbname}_for_test')

#  创建数据库 k_house 的连接 
conn2, curs2, engine2 = common_db.creat_conn_with_pg(dbname=dbname)

table_name = 'stock_zh_a_spot_test'

stock_zh_a_spot_df.to_sql(table_name,
          engine2,
          index     = False,
          if_exists = 'replace')    # 写入数据库  还有一个参数是  append，那是附加在表后
# 添加索引
# curs2.execute("""CREATE  INDEX parallel_tool_1      ON  parallel_tool_并行任务分配信息表  (交易日期); 
#                 CREATE  INDEX parallel_tool_2      ON  parallel_tool_并行任务分配信息表  (分组序号);
#                 CREATE  INDEX parallel_tool_3      ON  parallel_tool_并行任务分配信息表  (处理状态);"""
#             )
# conn2.commit()

df = pd.read_sql_query(f"""
    SELECT *
    FROM  {table_name}
  """,
   # params = (date,),
  con = engine2,
)

df[:-5]

# 插入到 MySQL 数据库中
# common_db.insert_db(stock_zh_a_spot_df, "stock_zh_a_spot", True, "`symbol`")
