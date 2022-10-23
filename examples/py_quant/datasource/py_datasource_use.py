import time

import mplfinance as mpf

import sys
sys.path.append('/Users/afirez/studio/python/auto-trade/examples/py_quant/common')
sys.path.append('/Users/afirez/studio/python/auto-trade/examples/py_quant/common/common_pg.py')
sys.path.append('/Users/afirez/studio/python/auto-trade/modules/Ashare')
sys.path.append('/Users/afirez/studio/python/auto-trade/modules/Ashare/Ashare.py')

"""
1. 通用安装方法：pip install akshare  --upgrade
2. Python安装：pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
3. Anaconda 安装：pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --user  --upgrade

"""

import mplfinance as mpf
# 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
my_color = mpf.make_marketcolors(up='r',
                                 down='g',
                                 edge='inherit',
                                 wick='inherit',
                                 volume='inherit')
# 设置图表的背景色
my_style = mpf.make_mpf_style(marketcolors=my_color,
                              figcolor='(0.82, 0.83, 0.85)',
                              gridcolor='(0.82, 0.83, 0.85)')


# ===============表格美化输出===============
def df_table(df,index):
    import prettytable as pt
    #利用prettytable对输出结果进行美化,index为索引列名:df_table(df,'market')
    tb = pt.PrettyTable()
    df = df.reset_index(drop = True)
    tb.add_column(index,df.index)
    for col in df.columns.values:#df.columns.values的意思是获取列的名称
        tb.add_column(col, df[col])
    print(tb)


# 测试计时开始，测试哪个就把if 后面的0改为1即可，其它改成0。
time1 = time.time()
print('开始提取数据')

if 0:
    # 1.Tushare
    import tushare as ts
    pro = ts.pro_api('6a0899533f8a5996f738183dbdf63c0afb3fcc931f08e1233575a339')#token，请注册后替换为自己的token。
    df = pro.daily(ts_code='300750.SZ', start_date='20210101', end_date='20220715')
    print('Tushare行情获取\n',df)
    # 单次提取股票数据耗时: 1.0941672325134277 秒

if 0:
    # 2.AKshare
    import akshare as ak
    df = ak.stock_zh_a_hist(symbol="300750", period="daily", start_date="20210101", end_date='20220715', adjust="qfq")
    print('AKshare行情获取\n',df)
    # 单次提取股票数据耗时: 2.899998426437378 秒

if 0:
    # baostock
    import baostock as bs
    import pandas as pd
    lg = bs.login()
    rs = bs.query_history_k_data_plus("sz.300750",
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
        start_date='2021-01-01', end_date='2022-07-15',
        frequency="d", adjustflag="3")
    
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    df = pd.DataFrame(data_list, columns=rs.fields)
    
    bs.logout()
    print('baostock行情获取\n',df)
    # 单次提取股票数据耗时: 0.9699969291687012 秒
    
if 1:
    # 4.Ashare
    from  Ashare import *
    df=get_price('sz300750',frequency='1d',count=371)  #默认获取今天往前5天的日线实时行情,count=371，表示获取371根K线。
    print('Ashare行情获取\n',df)
    # 单次提取股票数据耗时: 0.9399988651275635 秒


if 0:
    # 5.Pytdx
    from pytdx.hq import TdxHq_API
    api = TdxHq_API()
    # 数据获取接口一般返回list结构，如果需要转化为pandas Dataframe接口，可以使用 api.to_df 进行转化
    with api.connect('119.147.212.81', 7709):
        df = api.to_df(api.get_security_bars(9, 0, '300750', 0, 371)) 
        print('pytdx行情获取\n',df)
        # 单次提取股票数据耗时: 0.9504680633544922 秒	

if __name__ == "__main__":

    df_table(df,'行情')
    time2 = time.time()
    print("单次提取股票数据耗时:",time2-time1,'秒')
    # df["time", "open","high","low","close","volume"] = df[["datetime", "open", "high", "low", "close", "vol"]]
    # df_table(df,'行情')
    mpf.plot(df.tail(120), style=my_style, type='candle',mav=(5,20,50), volume=True)


