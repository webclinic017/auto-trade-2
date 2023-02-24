import pyautogui

import atomac
from time import sleep
from atomac.AXKeyCodeConstants import *
import pandas as pd


# try:
#     import ldtp
# except ImportError:
#     import atomac.ldtp as ldtp

bundle_id = 'cn.com.htzq.macstock'

"""
pyautogui

win pywinauto

mac atomacos pip install atomacos

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
    # atomac.terminateAppByBundleId(bundle_id)
    atomac.launchAppByBundleId(bundle_id)
    sleep(1)
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)

    # part 2, 获取当前应用windows
    # window = atomac_windows(automator=automator)

    window = automator.windows()[0]
    print(window)
    print(window.AXPosition)
    print(window.AXSize)
    return automator, window



def atomac_windows(automator):
    # part 2, 获取当前应用windows
    window = automator.windows()[0]
    print(window)
    print(window.AXPosition)
    print(window.AXSize)
    return window

def login(account='', pwd='', extra = ''):
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)
    window = automator.windows()[0]

    l_AXTextField = window.findAll(AXRole='AXTextField')
    s1 = l_AXTextField[0]
    s2 = l_AXTextField[1]
    s3 = l_AXTextField[2]
    s1_p = s1.AXPosition
    s1_s = s1.AXSize
    s2_p = s2.AXPosition
    s2_s = s2.AXSize
    s3_p = s3.AXPosition
    s3_s = s3.AXSize
    s1.tripleClickMouse((s1_p[0] + s1_s[0] / 2, s1_p[1] + s1_s[1] / 2))
    s1.sendKeys(account)
    s2.tripleClickMouse((s2_p[0] + s1_s[0] / 2, s2_p[1] + s2_s[1] / 2))
    s2.sendKeys(pwd)
    s3.tripleClickMouse((s3_p[0] + s1_s[0] / 2, s3_p[1] + s3_s[1] / 2))
    s3.sendKeys(extra)

    # 查找元素
    wx = window.findFirstR(AXRole='AXButton', AXTitle='登 录')
    # wx = window.findFirstR(AXRole='AXButton', AXIdentifier=55)
    # print(wx)
    # print(wx.AXPosition)
    # print(wx.AXSize)
    # print(wx.AXIdentifier)
    # print(wx.getAttributes())
    wx.Press()
    # wx.clickMouseButtonLeft(wx.AXPosition)


def atomac_text_field_input(automator, window, account, pwd, extra):
    # part 6, 输入内容（输入键盘字符，US_keyboard）
    # s1 = window.findFirstR(AXRole='AXTextField', AXRoleDescription='请输入客户号')
    # s1 = window.findFirstR(AXRole='AXTextField', AXTitle='')
    # s1 = window.findFirstR(AXRole='AXTextField')
    l_AXTextField = window.findAll(AXRole='AXTextField')
    s1 = l_AXTextField[0]
    s2 = l_AXTextField[1]
    s3 = l_AXTextField[2]
    s1_p = s1.AXPosition
    s1_s = s1.AXSize
    s2_p = s2.AXPosition
    s2_s = s2.AXSize
    s3_p = s3.AXPosition
    s3_s = s3.AXSize
    s1.tripleClickMouse((s1_p[0] + s1_s[0] / 2, s1_p[1] + s1_s[1] / 2))
    s1.sendKeys('123456')
    s2.tripleClickMouse((s2_p[0] + s1_s[0] / 2, s2_p[1] + s2_s[1] / 2))
    s2.sendKeys('123456')
    s3.tripleClickMouse((s3_p[0] + s1_s[0] / 2, s3_p[1] + s3_s[1] / 2))
    s3.sendKeys('123456')



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

def get_balance():
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)
    window = automator.windows()[0]

    scroll_area = window.findAll(AXRole='AXScrollArea')[0]   
    parent = scroll_area

    # child = window.findAllR(AXRole='AXStaticText', AXValue='总资产')[0]
    # table = child.AXParent.AXParent.AXParent
    # parent = table

    list_AXStaticText = parent.findAllR(AXRole='AXStaticText') 
    list_account = [t.AXValue for t in list_AXStaticText]
    list_account = list_account[:-2]
    account = {}
    for i in range(0, int(len(list_account) / 2)):
        account[list_account[2*i]] = list_account[2*i -1]
    # account = {list_account[2*i]: list_account[2*i -1] for i in range(0, int(len(list_account) / 2))}
    print(account)
    return account 

    child = window.findAllR(AXRole='AXStaticText', AXValue='总资产')[0]
    table = child.AXParent.AXParent.AXParent
    # table = btn_buy_1.AXParent
    # table = btn_buy_reset.AXParent
    print("parent")
    print(table)

    for child1 in table.AXChildren:
        print("child1")
        print(child1)

        if not child1.AXChildren:
            continue

        for child2 in child1.AXChildren:
            print("child2")
            print(child2)

            if not child2.AXChildren:
                continue

            for child3 in child2.AXChildren:
                print("child3")
                print(child3)

def bid_5():
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)
    window = automator.windows()[0]

    scroll_area = window.findAll(AXRole='AXScrollArea')[1]   
    list_AXStaticText = scroll_area.findAllR(AXRole='AXStaticText') 
    list = [t.AXValue for t in list_AXStaticText]
    # list_account = list_account[:-2]
    bid = {}
    for i in range(0, int(len(list) / 2)):
        bid[list[2*i]] = list[2*i -1]
    # account = {list_account[2*i]: list_account[2*i -1] for i in range(0, int(len(list_account) / 2))}
    print(bid)

def ask_5():
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)
    window = automator.windows()[0]
    scroll_area = window.findAll(AXRole='AXScrollArea')[2]   
    list_AXStaticText = scroll_area.findAllR(AXRole='AXStaticText') 
    list = [t.AXValue for t in list_AXStaticText]
    # list_account = list_account[:-2]
    ask = {}
    for i in range(0, int(len(list) / 2)):
        ask[list[2*i]] = list[2*i -1]
    # account = {list_account[2*i]: list_account[2*i -1] for i in range(0, int(len(list_account) / 2))}
    print(ask)

def get_positions():
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)

    window = automator.windows()[0]
    scroll_area = window.findAll(AXRole='AXScrollArea')[3]   
    ax_group = scroll_area.findFirstR(AXRole='AXGroup') 
    # print(ax_group.getAttributes())
    # print(ax_group.AXChildren[0].getAttributes())
    columes = [t.AXTitle  for t in ax_group.AXChildren]
    print(columes)
    list_AXRow = scroll_area.findAllR(AXRole='AXRow') 
    # print(list_AXRow)
    # print(list_AXRow[0].getAttributes())
    # print(list_AXRow[0].AXChildren[0].getAttributes())
    data = [[st.AXValue for st in row.AXChildren] for row in list_AXRow]
    print(data)

    return columes, data

def get_orders():
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)
    window = automator.windows()[0]

    btn_stock = window.findFirstR(AXRole='AXButton', AXTitle='股票')
    # btn_buy = window.findFirstR(AXRole='AXButton', AXTitle='买入')
    # btn_sell = window.findFirstR(AXRole='AXButton', AXTitle='卖出')
    # btn_hold = window.findFirstR(AXRole='AXButton', AXTitle='持仓')
    btn_to_buy = window.findFirstR(AXRole='AXButton', AXTitle='委托')
    btn_all = window.findFirstR(AXRole='AXStaticText', AXValue='只显示可撤委托')
    # btn_buy_done = window.findFirstR(AXRole='AXButton', AXTitle='成交')
    # btn_details = window.findFirstR(AXRole='AXButton', AXTitle='资金明细')
    btn_stock.Press()
    btn_to_buy.Press()

    # scroll_area = window.findAll(AXRole='AXScrollArea')[0]   
    # parent = scroll_area

    # child = window.findAllR(AXRole='AXStaticText', AXValue='总资产')[0]
    # table = child.AXParent.AXParent.AXParent
    # parent = table

    # list_AXStaticText = parent.findAllR(AXRole='AXStaticText') 
    # list_account = [t.AXValue for t in list_AXStaticText]
    # list_account = list_account[:-2]
    # account = {}
    # for i in range(0, int(len(list_account) / 2)):
    #     account[list_account[2*i]] = list_account[2*i -1]
    # # account = {list_account[2*i]: list_account[2*i -1] for i in range(0, int(len(list_account) / 2))}
    # print(account)

    # return account 

    check_boxes = window.findAllR(AXRole='AXCheckBox')
    print(check_boxes[0].AXValue)
    if check_boxes[0].AXValue == 1:
        check_boxes[0].Press()

    like = window.findAllR(AXRole='AXButton', AXTitle='委托日期')[0]
    columns = [child.AXTitle for child in like.AXParent.AXChildren]
    print(columns)

    parent = like.AXParent.AXParent
    rows = parent.findAllR(AXRole='AXRow')

    data = [[child.AXValue for child in row.AXChildren] for row in rows]
    print(data)

    return columns, data

    # parent = btn_buy_1.AXParent
    # parent = btn_buy_reset.AXParent
    print("parent")
    print(parent)

    parent = btn_all.AXParent

    for child1 in parent.AXChildren:
        print("child1")
        print(child1)

        if not child1.AXChildren:
            continue

        for child2 in child1.AXChildren:
            print("child2")
            print(child2)

            if not child2.AXChildren:
                continue

            for child3 in child2.AXChildren:
                print("child3")
                print(child3)

def get_trades():
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)
    window = automator.windows()[0]

    btn_stock = window.findFirstR(AXRole='AXButton', AXTitle='股票')
    # btn_buy = window.findFirstR(AXRole='AXButton', AXTitle='买入')
    # btn_sell = window.findFirstR(AXRole='AXButton', AXTitle='卖出')
    # btn_hold = window.findFirstR(AXRole='AXButton', AXTitle='持仓')
    # btn_to_buy = window.findFirstR(AXRole='AXButton', AXTitle='委托')
    btn_buy_done = window.findFirstR(AXRole='AXButton', AXTitle='成交')
    # btn_details = window.findFirstR(AXRole='AXButton', AXTitle='资金明细')
    btn_stock.Press()
    btn_buy_done.Press()

    # scroll_area = window.findAll(AXRole='AXScrollArea')[0]   
    # parent = scroll_area

    # child = window.findAllR(AXRole='AXStaticText', AXValue='总资产')[0]
    # table = child.AXParent.AXParent.AXParent
    # parent = table

    # list_AXStaticText = parent.findAllR(AXRole='AXStaticText') 
    # list_account = [t.AXValue for t in list_AXStaticText]
    # list_account = list_account[:-2]
    # account = {}
    # for i in range(0, int(len(list_account) / 2)):
    #     account[list_account[2*i]] = list_account[2*i -1]
    # # account = {list_account[2*i]: list_account[2*i -1] for i in range(0, int(len(list_account) / 2))}
    # print(account)

    # return account 

    like = window.findAllR(AXRole='AXButton', AXTitle='成交日期')[0]
    columns = [child.AXTitle for child in like.AXParent.AXChildren]
    print(columns)

    parent = like.AXParent.AXParent
    rows = parent.findAllR(AXRole='AXRow')
    data = [[child.AXValue for child in row.AXChildren] for row in rows]
    print(data)

    return columns, data

    # parent = btn_buy_1.AXParent
    # parent = btn_buy_reset.AXParent
    print("parent")
    print(parent)

    for child1 in parent.AXChildren:
        print("child1")
        print(child1)

        if not child1.AXChildren:
            continue

        for child2 in child1.AXChildren:
            print("child2")
            print(child2)

            if not child2.AXChildren:
                continue

            for child3 in child2.AXChildren:
                print("child3")
                print(child3)

def buy(code, price, amount):
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)

    window = automator.windows()[0]

    while True:
        btn_1 =  window.findFirstR(AXRole='AXButton', AXTitle='确认')
        btn_2 = window.findFirstR(AXRole='AXButton', AXValue='是')
        
        if btn_1:
            btn_1.Press()
            sleep(0.2)
            continue
        elif btn_2:
            btn_2.Press()
            sleep(0.2)
            continue
        else:
            break

    # btn_trade = window.findFirstR(AXRole='AXButton', AXTitle='交易')
    # btn_trade.Press()
    btn_stock = window.findFirstR(AXRole='AXButton', AXTitle='股票')
    btn_stock.Press()
    btn_buy = window.findFirstR(AXRole='AXButton', AXTitle='买入')
    # btn_sell = window.findFirstR(AXRole='AXButton', AXTitle='卖出')
    btn_buy.Press()
    btn_buy_1 = window.findFirstR(AXRole='AXButton', AXTitle='确定买入')
    # btn_buy_reset = window.findFirstR(AXRole='AXButton', AXTitle='重填')


    list_AXTextField = window.findAllR(AXRole='AXTextField')
    s1 = list_AXTextField[1] #  code
    s2 = list_AXTextField[0] #  price
    s3 = list_AXTextField[2] #  amount

    s1_p = s1.AXPosition
    s1_s = s1.AXSize

    s2_p = s2.AXPosition
    s2_s = s2.AXSize

    s3_p = s3.AXPosition
    s3_s = s3.AXSize

    s1.tripleClickMouse((s1_p[0] + s1_s[0] / 2, s1_p[1] + s1_s[1] / 2))
    s1.sendKeys(str(code))

    s3.tripleClickMouse((s3_p[0] + s1_s[0] / 2, s3_p[1] + s3_s[1] / 2))
    s3.sendKeys(str(amount))

    s2.tripleClickMouse((s2_p[0] + s1_s[0] / 2, s2_p[1] + s2_s[1] / 2))
    s2.sendKeys(str(price))

    print([t.AXValue for t in list_AXTextField])
    btn_buy_1.Press()

    window.sendKeys([RETURN])
    sleep(0.1)
    window.sendKeys([RETURN])

    sleep(0.8)
    while True:
        btn_1 =  window.findFirstR(AXRole='AXButton', AXTitle='确认')
        btn_2 = window.findFirstR(AXRole='AXButton', AXValue='是')
        
        if btn_1:
            btn_1.Press()
            sleep(0.2)
            continue
        elif btn_2:
            btn_2.Press()
            sleep(0.2)
            continue
        else:
            break

    return
    table = window.findAllR(AXRole='AXStaticText', AXValue='价格')[0]

    table = table.AXParent
    # table = btn_buy_1.AXParent
    # table = btn_buy_reset.AXParent
    print("parent")
    print(table)

    for child1 in table.AXChildren:
        print("child1")
        print(child1)

        if not child1.AXChildren:
            continue

        for child2 in child1.AXChildren:
            print("child2")
            print(child2)

            if not child2.AXChildren:
                continue

            for child3 in child2.AXChildren:
                print("child3")
                print(child3)

def sell(code, price, amount):
    automator = atomac.getAppRefByBundleId(bundle_id)
    print(automator)

    window = automator.windows()[0]

    while True:
        btn_1 =  window.findFirstR(AXRole='AXButton', AXTitle='确认')
        btn_2 = window.findFirstR(AXRole='AXButton', AXValue='是')
        
        if btn_1:
            btn_1.Press()
            sleep(0.2)
            continue
        elif btn_2:
            btn_2.Press()
            sleep(0.2)
            continue
        else:
            break

    # btn_trade = window.findFirstR(AXRole='AXButton', AXTitle='交易')
    # btn_trade.Press()
    btn_stock = window.findFirstR(AXRole='AXButton', AXTitle='股票')
    btn_stock.Press()
    # btn_buy = window.findFirstR(AXRole='AXButton', AXTitle='买入')
    btn_buy = window.findFirstR(AXRole='AXButton', AXTitle='卖出')
    btn_buy.Press()
    # btn_buy_1 = window.findFirstR(AXRole='AXButton', AXTitle='确定买入')
    btn_buy_1 = window.findFirstR(AXRole='AXButton', AXTitle='确定卖出')
    # btn_buy_reset = window.findFirstR(AXRole='AXButton', AXTitle='重填')


    list_AXTextField = window.findAllR(AXRole='AXTextField')
    s1 = list_AXTextField[1] #  code
    s2 = list_AXTextField[0] #  price
    s3 = list_AXTextField[2] #  amount

    s1_p = s1.AXPosition
    s1_s = s1.AXSize

    s2_p = s2.AXPosition
    s2_s = s2.AXSize

    s3_p = s3.AXPosition
    s3_s = s3.AXSize

    s1.tripleClickMouse((s1_p[0] + s1_s[0] / 2, s1_p[1] + s1_s[1] / 2))
    s1.sendKeys(str(code))

    s3.tripleClickMouse((s3_p[0] + s1_s[0] / 2, s3_p[1] + s3_s[1] / 2))
    s3.sendKeys(str(amount))

    s2.tripleClickMouse((s2_p[0] + s1_s[0] / 2, s2_p[1] + s2_s[1] / 2))
    s2.sendKeys(str(price))
    print([t.AXValue for t in list_AXTextField])

    btn_buy_1.Press()
    window.sendKeys([RETURN])
    # sleep(0.1)
    window.sendKeys([RETURN])
    # automator.sendKeys([RETURN])
    # automator.sendKeys([RETURN])
    sleep(0.8)
    while True:
        btn_1 =  window.findFirstR(AXRole='AXButton', AXTitle='确认')
        btn_2 = window.findFirstR(AXRole='AXButton', AXValue='是')
        
        if btn_1:
            btn_1.Press()
            sleep(0.2)
            continue
        elif btn_2:
            btn_2.Press()
            sleep(0.2)
            continue
        else:
            break

    return



def test():
    automator, window = open_app()
    window = automator.windows()[0]
    btn_stock = window.findFirstR(AXRole='AXButton', AXTitle='股票')
    btn_buy = window.findFirstR(AXRole='AXButton', AXTitle='买入')
    btn_sell = window.findFirstR(AXRole='AXButton', AXTitle='卖出')
    btn_hold = window.findFirstR(AXRole='AXButton', AXTitle='持仓')
    btn_to_buy = window.findFirstR(AXRole='AXButton', AXTitle='委托')
    btn_buy_done = window.findFirstR(AXRole='AXButton', AXTitle='成交')
    btn_details = window.findFirstR(AXRole='AXButton', AXTitle='资金明细')
    
    btn_map = {
        "股票": btn_stock,
        "买入": btn_buy,
        "卖出": btn_sell,
        "持仓": btn_hold,
        "委托": btn_to_buy,
        "成交": btn_buy_done,
        "资金明细": btn_details,
    }
    btn_map['持仓'].Press()

    # 获取滚动区域对象
    # balance
    scroll_area = window.findAll(AXRole='AXScrollArea')[0]   
    list_AXStaticText = scroll_area.findAllR(AXRole='AXStaticText') 
    list_account = [t.AXValue for t in list_AXStaticText]
    list_account = list_account[:-2]
    account = {}
    for i in range(0, int(len(list_account) / 2)):
        account[list_account[2*i]] = list_account[2*i -1]
    # account = {list_account[2*i]: list_account[2*i -1] for i in range(0, int(len(list_account) / 2))}
    print(account)

    # bid
    scroll_area = window.findAll(AXRole='AXScrollArea')[1]   
    list_AXStaticText = scroll_area.findAllR(AXRole='AXStaticText') 
    list_account = [t.AXValue for t in list_AXStaticText]
    # list_account = list_account[:-2]
    account = {}
    for i in range(0, int(len(list_account) / 2)):
        account[list_account[2*i]] = list_account[2*i -1]
    # account = {list_account[2*i]: list_account[2*i -1] for i in range(0, int(len(list_account) / 2))}
    print(account)
    
    # ask
    scroll_area = window.findAll(AXRole='AXScrollArea')[2]   
    list_AXStaticText = scroll_area.findAllR(AXRole='AXStaticText') 
    list = [t.AXValue for t in list_AXStaticText]
    # list_account = list_account[:-2]
    bid = {}
    for i in range(0, int(len(list) / 2)):
        bid[list[2*i]] = list[2*i -1]
    # account = {list_account[2*i]: list_account[2*i -1] for i in range(0, int(len(list_account) / 2))}
    print(bid)

    # ask
    scroll_area = window.findAll(AXRole='AXScrollArea')[3]   
    list_AXStaticText = scroll_area.findAllR(AXRole='AXStaticText') 
    list = [t.AXValue for t in list_AXStaticText]
    # list_account = list_account[:-2]
    ask = {}
    for i in range(0, int(len(list) / 2)):
        ask[list[2*i]] = list[2*i -1]
    # account = {list_account[2*i]: list_account[2*i -1] for i in range(0, int(len(list_account) / 2))}
    print(ask)

    scroll_area = window.findAll(AXRole='AXScrollArea')[3]   
    ax_group = scroll_area.findFirstR(AXRole='AXGroup') 
    # print(ax_group.getAttributes())
    # print(ax_group.AXChildren[0].getAttributes())
    position_columes = [t.AXTitle  for t in ax_group.AXChildren]
    print(position_columes)
    list_AXRow = scroll_area.findAllR(AXRole='AXRow') 
    # print(list_AXRow)
    # print(list_AXRow[0].getAttributes())
    # print(list_AXRow[0].AXChildren[0].getAttributes())
    list_position = [[st.AXValue for st in row.AXChildren] for row in list_AXRow]
    print(list_position)

    print(scroll_area.getAttributes())
    for child in scroll_area.AXChildren:
        print('1')
        print(child)
        # print(child.getAttributes())
        for child2 in child.AXChildren:
            print('2')
            print(child2)
            # print(child2.AXRoleDescription)
            # print(child2.AXIdentifier)
            # print(child2.getAttributes())
            if not child2.AXChildren:
                continue

            for child3 in child2.AXChildren:
                print('3')
                print(child3)
                if not child3.AXChildren:
                    continue

                # print(child3.getAttributes())
                for child4 in child3.AXChildren:
                    print('4')
                    print(child4)
                    # print(child4.getAttributes())


if __name__ == '__main__':
    # test()
    # automator, window = open_app()

    # login(account="123456", pwd='123456', extra='123456')

    # get_balance()

    # columns, data = get_positions()
    # df = pd.DataFrame(data, columns=columns)
    # print(df)

    columns, data = get_orders()
    df = pd.DataFrame(data, columns=columns)
    print(df)

    # columns, data = get_trades()
    # df = pd.DataFrame(data, columns=columns)
    # print(df)

    # buy("000001", 11.0, 100)
    # sell("000001", 20.0, 100)

 

