# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 22:20:26 2020

@author: Jerry Chen
"""
'''
使用方法:
    1.打开下单程序，并将下单程序移动到左上角，窗口左上角应准确放到0,0点。
    2.将鼠标要点击功能的大致中点，记下鼠标坐标。
    3.将坐标填到相应功能的坐标位置，全部填完即可。
'''


import pyautogui, sys
print('Press Ctrl-C to quit.')
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)+'\n'
        print(positionStr, end='')
        
except KeyboardInterrupt:
    print('\n')