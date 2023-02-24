"""
Created on Mon Mar 30 16:15:35 2020

@author: Jerry  Chen
"""
# -*- coding: utf-8 -*-

import os
import time
import pyautogui
import pandas as pd
import win32gui
import win32con

""" 这里定义各个功能在界面上的相对坐标，以下单程序的左上角为零点。
       大家注意，这些坐标是以作者的电脑显示结果生成的，如果在大家电脑上
       运行不对，请修改相应坐标。本程序提供一个实时抓取鼠标坐标的代码，
       具体使用方法见getmousepos.py
"""
#===这下面的坐标的标准界面的坐标值，如果大家的windows界面没有放大显示，可以直接使用
'''
buyfunc=pd.DataFrame([['F1',46,86],
                   ['code',326,132],
                   ['price',326,166],
                   ['count',324,223],
                   ['buybutton',346,250]],
                  columns=['function','xpos','ypos'])
sellfunc=pd.DataFrame([['F2',46,103],
                   ['code',326,123],
                   ['price',326,160],
                   ['count',324,216],
                   ['buybutton',343,241]],
                  columns=['function','xpos','ypos'])
gethold=pd.DataFrame([['F4',80,220],
                   ['save',746,422],],
                  columns=['function','xpos','ypos'])
'''
#=============================================================================

buyfunc = pd.DataFrame([['F1', 59, 108],
                   ['code', 409, 157],
                   ['price', 403, 204],
                   ['count', 404, 273],
                   ['buybutton', 429, 304]],
                  columns=['function', 'xpos', 'ypos'])
sellfunc = pd.DataFrame([['F2', 63, 131],
                   ['code', 409, 156],
                   ['price', 400, 201],
                   ['count', 400, 273],
                   ['sellbutton', 431, 302]],
                  columns=['function', 'xpos', 'ypos'])
gethold = pd.DataFrame([['F4', 94, 281],
                   ['save', 346, 341], ],
                  columns=['function', 'xpos', 'ypos'])


class ThsTrader(object):
   """一个极简的同花顺自动下单工具，基于pyautogui实现"""
   
   
   def __init__(self):
        self.savepath = r'D:\我的文档\table.xls'
        #因为保存持仓保存位置默认位置不一致，为尽量让程序简单，不做保存到其他位置的
        #操作，如果gethold函数无法正确返回，大家需要修改这个字符串为你们本机下单软件
        #默认保存位置。
        self.thstoken = 'thstoken.png'
        #下单程序的一部分图像，用于在屏幕上定位下单程序
        self.winposx = 0
        self.winposy = 0
        self.hwnd_title = dict()
        #程序位置保存在这里

   def __returnOrgStatus__(self):
       #以防有其他窗口，清除掉，再点击F4功能
       pyautogui.press('esc', presses=2)
       time.sleep(0.5)
       #pyautogui.press( 'F4',presses=2)
       x = gethold['xpos'].iloc[0]+self.winposx
       y = gethold['ypos'].iloc[0]+self.winposy
       pyautogui.click(x, y)

   def __get_all_hwnd__(self, hwnd, mouse):
       if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

   def __BringToTop__(self):
       
       ret = False
       win32gui.EnumWindows(self.__get_all_hwnd__, 0)
       for h, t in self.hwnd_title.items():
           if t is not "" and t.find('网上股票交易系统', 0, len(t))!=-1:
               win32gui.SetForegroundWindow(h)
               ret = True
           #print(h, t)
       return ret

   def InitThs(self):
       
       #im = pyautogui.screenshot('thstoken.png',region=(0,0, 150, 200))
       self.__BringToTop__()
       WindowsPos = pyautogui.locateOnScreen(self.thstoken, confidence=0.9)
       if WindowsPos == None:
           pyautogui.alert("同花顺交易终端未打开或未放到桌面，请重试！")
           return False
       else:
           self.winposx = WindowsPos.left
           self.winposy = WindowsPos.top
           return True

   def GetHold(self):      
       #不管在不在前台，将下单程序调到前台
       self.__BringToTop__()
        
        #如果文件已存在，保存时会弹出一个确认窗口，为简便程序，先删除文件
       if os.path.exists(self.savepath)==True:
            os.remove(self.savepath)
            print(self.savepath)
        #step 1, click F4 function
       x=gethold['xpos'].iloc[0]+self.winposx
       y=gethold['ypos'].iloc[0]+self.winposy
       pyautogui.click(x, y)
       time.sleep(0.5)
       #setp 2, press control-s
       x=gethold['xpos'].iloc[1]+self.winposx
       y=gethold['ypos'].iloc[1]+self.winposy
       pyautogui.click(x, y)
       pyautogui.hotkey('ctrl', 's')
       time.sleep(0.5)
       #setp 3,press save button
       pyautogui.hotkey('alt', 's')
       time.sleep(0.5)
       holds=pd.read_csv(self.savepath,sep='\x09',encoding = "gbk")
       print(holds)
       #返回hold是格式为dataframe，结构和同花顺显示一致。
       return holds
   
   def RunBuy(self,tscode='000000',price='0.00',count='0'):
       self.__BringToTop__()
       #step 1, click F1 function
       x=buyfunc['xpos'].iloc[0]+self.winposx 
       y=buyfunc['ypos'].iloc[0]+self.winposy
       pyautogui.click(x, y)
       #setp 2, click code input box and input code
       x=buyfunc['xpos'].iloc[1]+self.winposx 
       y=buyfunc['ypos'].iloc[1]+self.winposy
       pyautogui.click(x, y)
       time.sleep(0.5)
       pyautogui.press( 'backspace',presses=6)
       pyautogui.press( 'del',presses=6)
       time.sleep(0.5)
       pyautogui.write(tscode) 
       #setp 3,input buy price
       x=buyfunc['xpos'].iloc[2]+self.winposx
       y=buyfunc['ypos'].iloc[2]+self.winposy
       pyautogui.click(x, y)
       time.sleep(0.5)
       pyautogui.press( 'backspace',presses=6)
       pyautogui.press( 'del',presses=6)
       time.sleep(0.5)
       pyautogui.write(price) 
       #setp 4,input buy count
       x=buyfunc['xpos'].iloc[3]+self.winposx
       y=buyfunc['ypos'].iloc[3]+self.winposy
       pyautogui.click(x, y)
       time.sleep(0.5)
       pyautogui.press( 'backspace',presses=6)
       pyautogui.press( 'del',presses=6)
       time.sleep(0.5)
       pyautogui.write(count) 
       #setp 5,click buy button
       x=buyfunc['xpos'].iloc[4]+self.winposx
       y=buyfunc['ypos'].iloc[4]+self.winposy
       # pyautogui.click(x, y)
       time.sleep(2)
       pyautogui.hotkey('alt', 'y')
       #make interface to original status
       self.__returnOrgStatus__()
    
    
   def RunSell(self,tscode='000000',price='0.00',count='0'):
       self.__BringToTop__()
       #step 1, click F1 function
       x=sellfunc['xpos'].iloc[0]+self.winposx
       y=sellfunc['ypos'].iloc[0]+self.winposy
       pyautogui.click(x, y)
       time.sleep(0.5)
       #setp 2, click code input box and input code
       x=sellfunc['xpos'].iloc[1]+self.winposx
       y=sellfunc['ypos'].iloc[1]+self.winposy
       pyautogui.click(x, y)
       time.sleep(0.5)
       pyautogui.press( 'backspace',presses=6)
       pyautogui.press( 'del',presses=6)
       time.sleep(0.5)
       pyautogui.write(tscode) 
       #setp 3,input buy price
       x=sellfunc['xpos'].iloc[2]+self.winposx
       y=sellfunc['ypos'].iloc[2]+self.winposy
       pyautogui.click(x, y)
       time.sleep(0.5)
       pyautogui.press( 'backspace',presses=6)
       pyautogui.press( 'del',presses=6)
       time.sleep(0.5)
       pyautogui.write(price) 
       #setp 4,input buy count
       x=sellfunc['xpos'].iloc[3]+self.winposx
       y=sellfunc['ypos'].iloc[3]+self.winposy
       pyautogui.click(x, y)
       time.sleep(0.5)
       pyautogui.press( 'backspace',presses=6)
       pyautogui.press( 'del',presses=6)
       time.sleep(0.5)
       pyautogui.write(count) 
       #setp 5,click buy button
       x=sellfunc['xpos'].iloc[4]+self.winposx
       y=sellfunc['ypos'].iloc[4]+self.winposy
       # pyautogui.click(x, y)
       time.sleep(2)
       pyautogui.hotkey('alt', 'y')
       #make interface to original status
       self.__returnOrgStatus__()
        
if __name__ == "__main__":
    trader=ThsTrader()
    trader.InitThs()
        
    trader.GetHold()
    
    # trader.RunBuy("000001",'12.55','100')
    # trader.RunSell("000001",'12.55','100')