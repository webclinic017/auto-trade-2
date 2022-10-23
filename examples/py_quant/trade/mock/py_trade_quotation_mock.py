import pyautogui

import time

#爬新浪财经股票实时信息

import easyquotation

#数据处理

import pandas as pd

#数据可视化

import matplotlib.pyplot as plt

#量化分析

import quantstats as qs

import seaborn

from finta import TA

#统计分析

import statsmodels.api as sm

import PySimpleGUI as sg

import matplotlib.pyplot as plt

import mplfinance as mpf

import quantstats as qs

import pyttsx3

#驱动浏览器

time_data=[]

now_data=[]

Open_data=[]

close_data=[]

globallow_data=[]

high_data=[]

low_data=[]

buy_data=[]

sell_data=[]

turnover_data=[]

sell_1_volume_data=[]

sell_1_price_data=[]

buy_1_volume_data=[]

buy_1_price_data=[]

Volume_data=[]

cash_data=[]

money_data=[]

cksz_data=[]

fdyk_data=[]

fdykb_data=[]

xddjzj_data=[]

def get_stock_data(stock='600031'):

    #数据获取

    df=easyquotation.api.use('sina')

    data=df.real(stock)

    import time as ts

    loca=ts.localtime()

    year=loca.tm_year

    moth=loca.tm_mon

    day=loca.tm_mday

    #让数据形成序列

    

    #数据清洗

    #现在的价格，数据间隔3秒，3秒为一个bar,交易所3秒刷新一次数据

    #时间

    time=data[stock]['time']

    #现价

    now=data[stock]['now']

    #开盘价

    Open=data[stock]['open']

    #收盘价

    close=data[stock]['close']

    #最低价

    low=data[stock]['low']

    #最高价

    high=data[stock]['high']

    #现在的买价

    buy=data[stock]['buy']

    #限制的卖价

    sell=data[stock]['sell']

    #换手率

    turnover=data[stock]['turnover']

    #成交量

    Volume=data[stock]['volume']

    #一档卖成交量

    sell_1_volume=data[stock]['bid1_volume']

    #一档卖价

    sell_1_price=data[stock]['bid1']

    #一档买成交量

    buy_1_volume=data[stock]['ask1_volume']

    #一档买价

    buy_1_price=data[stock]['ask1']

    #添加数据

    time_data.append(str(year)+'-'+str(moth)+'-'+str(day)+'-'+str(time))

    now_data.append(now)

    Open_data.append(Open)

    close_data.append(close)

    low_data.append(low)

    high_data.append(high)

    buy_data.append(buy)

    sell_data.append(sell)

    turnover_data.append(turnover)

    Volume_data.append(Volume)

    sell_1_volume_data.append(sell_1_volume)

    sell_1_price_data.append(sell_1_price)

    buy_1_volume_data.append(buy_1_volume)

    buy_1_price_data.append(buy_1_price)

    df1=pd.DataFrame({'时间':time_data,'现价':now_data,'开盘价':Open_data,'收盘价':close_data,'最高价':high_data,'最低价':low_data,

    '买价':buy_data,'卖价':sell_data,'换手率':turnover_data,'成交量':Volume_data,'买一价格':buy_1_price_data,'买一量':buy_1_volume_data,

    '卖一价格':sell_1_price_data,'卖一量':sell_1_volume_data})

    #保持实时数据

    df1.to_excel(r'./data/股票数据.xlsx')

    print('股票数据输出完成')

    pyttsx3.speak('股票数据输出完成')