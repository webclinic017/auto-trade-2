from selenium import webdriver

import selenium

#启动火狐浏览器

#图形界面

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

def get_stock_plot():

    df1=pd.read_excel(r'C:\Users\Administrator\Desktop\股票数据.xlsx')

    df1.rename(columns={'时间':'Date','开盘价':'Open','收盘价':'Close','最高价':'High','最低价':'Low','成交量':'Volume'},inplace=True)

    #时间格式转换

    plt.rcParams['font.family']='SimHei'

    plt.rcParams['axes.unicode_minus']=False

    df1['Date']=pd.to_datetime(df1['Date'])

    #出现设置索引

    df1.set_index(['Date'],inplace=True)

    #设置股票颜

    mc=mpf.make_marketcolors(up='g',down='r',edge='i')

    #设置系统

    s=mpf.make_mpf_style(marketcolors=mc)

    add_plot=[mpf.make_addplot(df1['现价'],panel=1,title='now',color='r')]

    mpf.plot(df1,type='candle',style=s,mav=(5,10,20),addplot=add_plot)

    plt.show()

#绘制账户信息

def get_zf_plot():

    plt.rcParams['font.family']='SimHei'

    plt.rcParams['axes.unicode_minus']=False

    df=pd.read_excel(r'C:\Users\Administrator\Desktop\账户数据.xlsx')

    plt.plot(df['可用现金'],label='可用现价',color='r')

    plt.plot(df['总资产'],label='总资产',color='g')

    plt.plot(df['参考市值'],label='参考市值',color='y')

    plt.legend()

    plt.show()

#量化指标

def get_quantstats_any():

    df=pd.read_excel(r'C:\Users\Administrator\Desktop\股票数据.xlsx')

    df.rename(columns={'时间':'Date','开盘价':'Open','收盘价':'Close','最高价':'High','最低价':'Low','成交量':'Volume'},inplace=True)

    print(df)

    df['Date']=pd.to_datetime(df['Date'])

    #出现设置索引

    qs.extend_pandas()

    #指标报告

    stock=qs.reports.metrics(df['Close'])

    print(stock)

#绘制技术指标

def get_technology_zb():

    df=pd.read_excel(r'C:\Users\Administrator\Desktop\股票数据.xlsx')

    df.rename(columns={'开盘价':'Open','收盘价':'Close','最高价':'High','最低价':'Low','成交量':'Volume'},inplace=True)

    plt.rcParams['font.family']='SimHei'

    plt.rcParams['axes.unicode_minus']=False

    #出现设置索引

    del df['Date']

    df['Date']='2021-12-15'

    df.set_index(df['Date'],inplace=True)

    print(df)

    macd=TA.MACD(df)

    boll=TA.BBANDS(df)

    rsi=TA.RSI(df)

    plt.subplot(3,1,1)

    plt.title('MACD')

    plt.plot(macd['MACD'],label='MACD',color='r')

    plt.plot(macd['SIGNAL'],label='SIGNAL',color='y')

    plt.legend()

    plt.subplot(3,1,2)

    plt.title('RSI')

    plt.plot(rsi,label='RSI')

    plt.subplot(3,1,3)

    plt.title('BOLL')

    plt.plot(boll['BB_UPPER'],color='r',label='上轨线')

    plt.plot(boll['BB_MIDDLE'],label='中轨线',color='m')

    plt.plot(boll['BB_LOWER'],label='下轨线',color='g')

    plt.legend()

    plt.show()
