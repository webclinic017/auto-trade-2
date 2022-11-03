
import py_trade_quotation_mock as py_trade_quotation

import time

import pandas as pd

import py_trade_trader_mock as trader

import akshare as ak

import pyautogui

# trader.get_login()

import pyttsx3

while True:

    local=time.localtime()

    h=local.tm_hour

    m=local.tm_min

    if ((h>=9 and h<=11) or (h>=13 and h<15)):

        pyttsx3.speak('开盘中')

        df8=ak.stock_individual_fund_flow_rank(indicator='今日')

        df9=df8[5:6]

        stock=df9['代码'].to_list()[0]

        name=df9['名称'].to_list()[0]

        py_trade_quotation.get_stock_data()

        df=pd.read_excel(r'./data/股票数据.xlsx')

        df['ma5']=df['现价'].rolling(5).mean()

        now=df['现价'][-1:].mean()

        ma5=df['ma5'][-1:].mean()

        df['ma10']=df['现价'].rolling(10).mean()

        ma10=ma5=df['ma10'][-1:].mean()

        if ma5>=ma10:

            trader.sell(price=now)

        else:

            trader.buy(price=now)

        trader.get_zf_data()

        time.sleep(10)

    else:

        import time

        time.sleep(30)

        pyttsx3.speak('等待开盘')
