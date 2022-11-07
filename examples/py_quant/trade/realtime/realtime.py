import numpy as np
import pandas as pd

quote_columns = [
    "序号",
    "代码",
    "名称",
    "最新价",
    "涨跌幅",
    "涨跌额",
    "成交量",
    "成交额",
    "振幅",
    "最高",
    "最低",
    "今开",
    "昨收",
    "量比",
    "换手率",
    "市盈率-动态",
    "市净率",
    "总市值",
    "流通市值",
    "涨速",
    "5分钟涨跌",
    "60日涨跌幅",
    "年初至今涨跌幅",
]

order_columns = [
    'date', # 成交日期
    'time', # 成交时间
    'code', # 证劵代码
    'name', # 证劵名称
    'operation', # 操作
    'volume', # 成交数量
    'price', # 成交均价
    'amount', # 成交金额
    'contract_code', # 合同编号
    'trade_code', # 成交编号
]

code_details = [
    
]