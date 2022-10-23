import time
import akshare as ak
import pandas as pd
import sys
sys.path.append('/Users/afirez/studio/python/auto-trade/examples/py_quant/common')
sys.path.append('/Users/afirez/studio/python/auto-trade/examples/py_quant/common/common_pg.py')

print("sys.path:",sys.path)
import common_pg as common_db

print(ak.__version__)

"""
# akshare 获取股票数据

# 1. 获取所有股票代码和名称
# df_all = ak.stock_zh_a_spot_em()
# print(df_all)
# df_all = df_all[["代码","名称"]]

# df_all2 = ak.stock_info_a_code_name()
# print(df_all2)

# 2. 遍历所有股票数据 获取历史行情数据：如
# symbol="002594"
# 
# em
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date="20000301", end_date='20220729', adjust="")
# print(stock_zh_a_hist_df)
#
# sina
# stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol=symbol, adjust="qfq")

# 3. 实时股票数据
# em 分页数据一次性加载
# 0.5s
stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
print(stock_zh_a_spot_em_df)
# 
# sina 分页数据 慢
# stock_zh_a_spot_df = ak.stock_zh_a_spot()
# print(stock_zh_a_spot_df)
"""

"""
# easyquotation 获取股票数据
import easyquotation as eq
eq_sina = eq.use('sina') # 新浪 [sina] # 腾讯 [tencent, qq]
# 1.2s 分页数据 多线程
data_map = eq_sina.market_snapshot(prefix=False) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz /sh 前缀
data_map
#
# 单只股票
# data_map = eq_sina.real(['002594']) # 支持直接指定前缀，如 ‘sh000001’
# data_map
# 
# 多只股票
# data_map = eq_sina.stocks(['000001','002594'])
# data_map
"""

def app_run(): 
    while True:
        start_time = time.time()
        stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
        print(f'cost time: {time.time() - start_time}')
        print(stock_zh_a_spot_em_df)
        time.sleep(0.5)
        print(f'cost time with sleep: {time.time() - start_time}')

if __name__ == '__main__':
    app_run()