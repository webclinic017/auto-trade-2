import pandas as pd
from aip import AipOcr
import pyautogui
import pywinauto
import time
import ddddocr
import PIL
import akshare as ak
from PIL import Image,ImageDraw
import pyttsx3
from finta import TA
import quantstats as qs
import yagmail
import requests
from bs4 import BeautifulSoup
from lxml import etree

import schedule

import matplotlib.pyplot as plt
import mplfinance as mpf

app_id='252342421225'
api_key='grc71324214ewewlsl8zXo'
secret_key='ny8ClwdaLIDNaondoAINDOLH5jP9s6RbyG3'

"""
ocr
  easyocr: pip install easyocr
  chineseocr_lite:  git clone https://github.com/DayBreak-u/chineseocr_lite.git
  pytesseract (不推荐)
  百度OCR

"""

#登录同花顺期货通
def featurns_log():
    '''
    登录同花顺期货通，手动启动程序可以不用调用这个函数
    识别验证码自动登录
    '''
    import time
    pywinauto.application.Application(backend='uia').start(r'E:同花顺期货通binhapp.exe')
    pyttsx3.speak('运用启动成功')
    #等待程序
    time.sleep(1)
    #最大化窗口
    pyautogui.click(x=1379,y=18)
    time.sleep(1)
    #点击交易
    pyautogui.click(x=941,y=17)
    #选择模拟交易
    pyautogui.click(x=1065,y=53)

    time.sleep(1)

    pyautogui.click(x=1155,y=85)
    #等待程序响应
    time.sleep(3)
    #验证码区域截图
    pyautogui.screenshot(imageFilename=r'C:UsersAdministratorDesktop期货交易验证码.png',region=(1042,611,1099-1042,641-611))
    #识别验证码
    time.sleep(1)
    ocr=ddddocr.DdddOcr()
    with open(r'C:UsersAdministratorDesktop期货交易验证码.png','rb')as f:
        imag=f.read()
        result=ocr.classification(imag)
        pyttsx3.speak('验证码结果{}'.format(result))
    
    #输入验证码，先定位
    pyautogui.click(x=881,y=632)
    time.sleep(1)
    #输入验证码
    pyautogui.typewrite(result,interval=0.1)
    #点击登录
    time.sleep(1)
    pyautogui.click(x=950,y=722)
    pyttsx3.speak('登录成功')
    
#交易状态的识别,检测买入等交易是否成功
def featurns_trader_stats():
    '''
    交易状态的识别,检测买入等交易是否成功
    '''
    pyttsx3.speak('交易状态识别')
    pyautogui.screenshot(r'C:UsersAdministratorDesktop期货交易交易状态.png',region=(257,846,638-257,882-846))
    options={'language':'chn_eng'}
    aipcor=AipOcr(app_id,api_key,secret_key)
    image=open(r'C:UsersAdministratorDesktop期货交易交易状态.png','rb')
    image1=image.read()
    text_list=aipcor.general(image1,options=options)
    df1=pd.json_normalize(text_list['words_result'])
    df1.to_excel(r'C:UsersAdministratorDesktop期货交易交易状态.xlsx')
    df=pd.read_excel(r'C:UsersAdministratorDesktop期货交易交易状态.xlsx')
    df_words=df['words']
    text=df_words[0]+df_words[1]
    pyttsx3.speak('识别完成')
    pyttsx3.speak(text)

#建立多头头寸，买入
def featurns_buy(stock='cu2205',num='1'):
    '''
    stock='期货代码'
    num=买入的手数
    '''
    #点击输入
    pyttsx3.speak('开始买入建仓')
    pyautogui.click(x=320,y=649)
    #清楚数据
    pyttsx3.speak('开始清除')

    for i in range(6):
        pyautogui.press('backspace')

    pyttsx3.speak('清楚完成')
    pyttsx3.speak('开始输入')
    pyautogui.typewrite(stock,interval=0.001)
    pyautogui.press('enter')
    pyttsx3.speak('输入完成')
        
    #输入买入手数
    #开始清楚
    pyautogui.click(x=470,y=641)
    pyttsx3.speak('开始清除')
    for i in range(6):
        pyautogui.press('backspace')

    pyttsx3.speak('清除完成')
    pyautogui.typewrite(num,interval=0.001)
    pyttsx3.speak('开始输入')
    pyautogui.press('enter')
    pyttsx3.speak('输入完成')
    
    time.sleep(1)
    #点击买入/加多
    pyautogui.click(x=325,y=729)


featurns_trader_stats()

#识别合约信息
def exter_featurns_data():
    '''
    采用百度进行合约信息识别
    截图进行信息识别
    '''
    #缩小交易界面
    pyautogui.click(x=1309,y=533)
    time.sleep(1)
    
    #点击合约资料
    pyautogui.click(x=969,y=51)
    #信息截图
    time.sleep(1)
    pyautogui.screenshot(r'C:UsersAdministratorDesktop期货交易合约信息.png',region=(552,288,1675-552,520-288))
    options={'language':'chn_eng'}
    aipcor=AipOcr(app_id,api_key,secret_key)
    image=open(r'C:UsersAdministratorDesktop期货交易合约信息.png','rb')
    image1=image.read()
    text_list=aipcor.general(image1,options=options)
    df1=pd.json_normalize(text_list['words_result'])
    df1.to_excel(r'C:UsersAdministratorDesktop期货交易合约信息.xlsx')
    df=pd.read_excel(r'C:UsersAdministratorDesktop期货交易合约信息.xlsx')
    
    #将合约数据提取成表格数据
    df_words=df['words'][:11]
    data=[]
    col=[]
    
    for i in df_words.tolist():
        new_list=str(i).split(':')
        col.append(new_list[0])
        data.append(new_list[1])
    
    new_df=pd.DataFrame(data,col)
    print(new_df)
    pyttsx3.speak('合约数据提取成功')

#返回交易界面
def return_trader():
    '''
    返回交易界面
    '''
    pyautogui.click(x=941,y=17)
    #选择模拟交易
    pyautogui.click(x=1065,y=53)
    time.sleep(1)
    pyautogui.click(x=1155,y=85)
    pyttsx3.speak('返回交易界面成功')

#关掉交易界面
def close_trader():
    '''
    关掉交易界面
    '''
    pyautogui.click(x=1301,y=487)
    pyttsx3.speak('交易界面关闭成功')

#识别期货结算套保数据
def featurns_js_td():
    '''
    利用百度进行期货阶数套保数据识别
    '''
    #点击合约资料
    pyautogui.click(x=969,y=51)
    #信息截图
    time.sleep(1)
    #点击结算套保
    pyautogui.click(x=1343,y=151)
    time.sleep(1)
    pyautogui.screenshot(r'C:UsersAdministratorDesktop期货交易结算套保.png',region=(553,293,1671-553,639-293))
    
    options={'language':'chn_eng'}
    aipcor=AipOcr(app_id,api_key,secret_key)
    image=open(r'C:UsersAdministratorDesktop期货交易结算套保.png','rb')
    image1=image.read()
    text_list=aipcor.general(image1,options=options)
    df1=pd.json_normalize(text_list['words_result'])
    df1.to_excel(r'C:UsersAdministratorDesktop期货交易结算套保.xlsx')
    df=pd.read_excel(r'C:UsersAdministratorDesktop期货交易结算套保.xlsx')