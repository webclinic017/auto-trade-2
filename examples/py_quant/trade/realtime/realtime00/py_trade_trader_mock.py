from selenium import webdriver

import pyttsx3

import selenium

#启动火狐浏览器

#图形界面

import pyautogui

import os
import platform
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

import pyautogui

#驱动浏览器

cash_data=[]

money_data=[]

cksz_data=[]

fdyk_data=[]

fdykb_data=[]

xddjzj_data=[]

def get_driver():
    os_type = platform.system()
    # root_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname("./")
    # drivers_dir = os.path.join(root_dir, 'drivers')
    drivers_dir = os.path.dirname("/Users/afirez/studio/python/auto-trade/examples/weixin/drivers/")
    if os_type == 'Darwin':
        return os.path.join(drivers_dir, 'chromedriver_mac64')
    elif os_type == 'Windows':
        return os.path.join(drivers_dir, 'chromedriver_win32.exe')
    elif os_type == 'Linux':
        return os.path.join(drivers_dir, 'chromedriver_linux64')
    else:
        return None

driver_location = get_driver()
if driver_location is None:
    print('chromedriver 不支持的系统类型！')
    exit(-1)

global driver

# driver=webdriver.Firefox()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
driver = webdriver.Chrome(driver_location,chrome_options=chrome_options)

def get_login():

    import time

    #打开东方财富模拟交易界面

    driver.get(r'http://group.eastmoney.com/room/index.html')

    #最大浏览器

    driver.maximize_window()

    time.sleep(3)

    #点击登录，打开东方财富扫码登陆

    pyautogui.click(x=1148,y=894)

    time.sleep(10)

    print('登录成功')

    pyttsx3.speak('登录成功')

#买入程序

def buy(code='600031',volume=100,price=23):

    import time

    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="futcode"]').clear()

    driver.find_element_by_xpath('//*[@id="futcode"]').send_keys(code)

    time.sleep(1)

    #买入的价格

    driver.find_element_by_xpath('//*[@id="price"]').clear()

    driver.find_element_by_xpath('//*[@id="price"]').send_keys(price)

    #买入的数量

    driver.find_element_by_xpath('//*[@id="codenumber"]').clear()

    driver.find_element_by_xpath('//*[@id="codenumber"]').send_keys(volume)

    time.sleep(1)

    #点击买入，完成交易

    driver.find_element_by_xpath('//*[@id="btnOrder"]').click()

    #类型

    print('买入成功，股票代码{},数量{}，价格{}'.format(code,volume,price))

    pyttsx3.speak('买入成功，股票代码{},数量{}，价格{}'.format(code,volume,price))

    #刷新浏览器

    driver.refresh()

    #图像界面买单

    #卖出程序

def sell(code='600031',price=23,volume=100):

    #点击卖出

    driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[1]/div[3]/div[3]/div[3]/div[1]/div[1]/span[2]').click()

    #可卖出股票数量

    kymcgp=driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[1]/div[3]/div[3]/div[3]/div[1]/div[3]/div/i').text

    if int(kymcgp)>0:

         #如果股票数量小于100，一次性卖出

        if int(kymcgp)>0 and int(kymcgp)<100:

            volume=int(kymcgp)

        import time

        time.sleep(1)

        driver.find_element_by_xpath('//*[@id="main"]/div[5]/div[1]/div[3]/div[3]/div[3]/div[1]/div[1]/span[2]').click()

        driver.find_element_by_xpath('//*[@id="futcode"]').clear()

        #输入股票代码

        driver.find_element_by_xpath('//*[@id="futcode"]').send_keys(code)

        driver.find_element_by_xpath('//*[@id="price"]').clear()

        time.sleep(1)

        #输入价格

        driver.find_element_by_xpath('//*[@id="price"]').send_keys(price)

        driver.find_element_by_xpath('//*[@id="codenumber"]').clear()

        time.sleep(1)

        #输入数量

        driver.find_element_by_xpath('//*[@id="codenumber"]').send_keys(volume)

        #点击卖出

        time.sleep(1)

        driver.find_element_by_xpath('//*[@id="btnOrder"]').click()

        print('卖出成功，股票代码{}，数量{}，价格{}'.format(code,volume,price))

        pyttsx3.speak('卖出成功，股票代码{}，数量{}，价格{}'.format(code,volume,price))

        time.sleep(1)

        #刷浏览器

        driver.refresh()

    else:

        print('没有可用卖出的股票')

        pyttsx3.speak('没有可用卖出的股票')

        driver.refresh()

    #撤单程序

def get_zf_data():

    cash=driver.find_element_by_css_selector('#bottom > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(2)').text

    #总资产

    money=driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[2]/table/tbody/tr/td[1]/span[2]').text

    #参考市值

    cksz=driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[2]/table/tbody/tr/td[3]/span[2]').text

    #浮动盈亏

    fdyk=driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[2]/table/tbody/tr/td[4]/span[2]').text

    #浮动盈亏比

    fdykb=driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[2]/table/tbody/tr/td[5]/span[2]').text

    #下单冻结资金

    xddjzj=driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[2]/table/tbody/tr/td[6]/span[2]').text

    cash_data.append(cash)

    money_data.append(money)

    cksz_data.append(cksz)

    fdyk_data.append(fdyk)

    fdykb_data.append(fdykb)

    xddjzj_data.append(xddjzj)

    #添加实时数据

    df2=pd.DataFrame({'可用现金':cash_data,'总资产':money_data,'参考市值':cksz_data,'浮动盈亏':fdyk_data,'浮动盈亏比':fdyk_data,'下单冻结资金':xddjzj_data})

    df2.to_excel(r'./data/账户数据.xlsx')

    print('账户数据输出完成')

    pyttsx3.speak('账户数据输出完成')

def sdcx():

    #点击挂单

    import time

    time.sleep(3)

    driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[1]/div[3]/div[3]/div[3]/div[2]/ul/li[1]')

    #检测是否有可撤的单

    txt=driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[1]/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]/ul[1]/li[7]/span').text 

    print('文本',txt)                          

    if txt=='撤单':

        #点击撤单

        driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div[1]/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]/ul/li[7]/span').click()

        driver.refresh()

        sg.popup('撤单成功')