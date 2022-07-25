#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import akshare as ak
import pandas as pd
import sys
sys.path.append('/Users/afirez/studio/python/auto-trade/examples/py_quant/common')
sys.path.append('/Users/afirez/studio/python/auto-trade/examples/py_quant/common/common_pg.py')

print("sys.path:",sys.path)

# import common.common_pg as common_db
import common_pg as common_db

print(ak.__version__)

# 历史行情数据
# 日频率
# 接口: stock_zh_a_daily
# 目标地址: https://finance.sina.com.cn/realstock/company/sh600006/nc.shtml(示例)
# 描述: A 股数据是从新浪财经获取的数据, 历史数据按日频率更新; 注意其中的 sh689009 为 CDR, 请 通过 stock_zh_a_cdr_daily 接口获取
# 限量: 单次返回指定 A 股上市公司指定日期间的历史行情日频率数据
# adjust=""; 默认为空: 返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据;

stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000002", adjust="")
print(stock_zh_a_daily_qfq_df)

stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000002", start_date="20200101", end_date="20210101", adjust="")
print(stock_zh_a_daily_qfq_df)

# 0. 准备工作

dbname = "k_house"
#   0.1 创建数据库连接

#  创建数据库 股票分析数据库 的连接 
# conn, curs, engine = common_db.creat_conn_with_pg(dbname=f'{dbname}_for_test')

#  创建数据库 k_house 的连接 
conn2, curs2, engine2 = common_db.creat_conn_with_pg(dbname=dbname)

table_name = 'stock_zh_a_daily_test'

stock_zh_a_daily_qfq_df.to_sql(table_name,
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


# 插入到 MySQL 数据库中
# common_db.insert_db(stock_zh_a_daily_qfq_df, "stock_zh_a_daily", True, "`symbol`")



