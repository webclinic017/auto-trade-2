import pyautogui

import atomac
from time import sleep
from atomac.AXKeyCodeConstants import *

# try:
#     import ldtp
# except ImportError:
#     import atomac.ldtp as ldtp

bundle_id = 'cn.com.htzq.macstock'

"""
pyautogui

win pywinauto

mac pyatom 
# Python2
sudo easy_install atomac

# Python3
pip3 install git+https://github.com/pyatom/pyatom/
cn.com.htzq.macstock
"""
def open_app():
    # bs = atomac.AXClasses.AXKeyCodeConstants.BACKSPACE
    # part 1, 启动应用并获取应用信息
    atomac.launchAppByBundleId(bundle_id)
    sleep(2)
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)

    # part 2, 获取当前应用windows
    # window = atomac_windows(automator=automator)

    window = automator.windows()[0]
    print(window)
    print(window.AXPosition)
    print(window.AXSize)


    # part 3, 查找元素
    atomac_button(automator=automator, window=window)

    atomac_text_field(automator=automator, window=window)



def atomac_windows(automator):
    # part 2, 获取当前应用windows
    window = automator.windows()[0]
    print(window)
    print(window.AXPosition)
    print(window.AXSize)
    return window

def atomac_button(automator, window):
    # part 3, 查找元素
    # findFirst，返回第一个匹配的元素
    # findFirstR，递归查找，返回第一个匹配的元素（当查找的元素Parent非标准窗口时使用）
    # 在AXClasses.py文件中可以找到很多已经定义好的方法
    # dt = window.radioButtonsR('地图')[0]   # 也可以
    # dt = window.findFirstR(AXRole='AXRadioButton', AXTitle='地图')
    # gj = window.findFirstR(AXRole='AXRadioButton', AXTitle='公交')
    # wx = window.findFirstR(AXRole='AXRadioButton', AXTitle='卫星')
    wx = window.findFirstR(AXRole='AXButton', AXTitle='登 录')
    # wx = window.findFirstR(AXRole='AXButton', AXIdentifier=55)
    print(wx)
    print(wx.AXPosition)
    print(wx.AXSize)
    print(wx.AXIdentifier)
    print(wx.getAttributes())
    # wx.Press()
    # wx.clickMouseButtonLeft(wx.AXPosition)

def atomac_text_field(automator, window):
    # part 6, 输入内容（输入键盘字符，US_keyboard）
    # 666632307673
    # s1 = window.findFirstR(AXRole='AXTextField', AXRoleDescription='请输入客户号')
    # s1 = window.findFirstR(AXRole='AXTextField', AXTitle='666632307673')
    # s1 = window.findFirstR(AXRole='AXTextField')
    l_AXTextField = window.findAll(AXRole='AXTextField')[0]
    s1 = l_AXTextField[0]
    # sheet = automator.sheetsR()[0]
    # sheet = window.sheets()[0]
    # s1 = sheet.FindAll(AXRole='AXTextField')[0]
    # s1 == s2
    # s2 = window.textFieldsR('搜索文本栏')[0]
    # s1_id = s1.AXId
    # print(s1_id)
    s1_p = s1.AXPosition
    s1_s = s1.AXSize
    s1.tripleClickMouse((s1_p[0] + s1_s[0] / 2, s1_p[1] + s1_s[1] / 2))
    s1.sendKeys('66663230767')

    #  输入键盘上的修饰符
    atomac_send_keys(automator, window, s1)

def atomac_send_keys(automator, window, e):
    # part 7, 输入键盘上的修饰符
    sleep(1)
    e.sendKeys([BACKSPACE])
    # 回车
    e.sendKeys([RETURN])


def lacate_app():
    # 找到同花顺窗口并将其设置为活动窗口    
    window_pos = pyautogui.locateOnScreen('./logo_htzj.jpeg')
    print(window_pos)
    if window_pos:
        window_center = pyautogui.center(window_pos)
    pyautogui.click(window_center.x, window_center.y)

if __name__ == '__main__':
    open_app()

