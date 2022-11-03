from pydoc import classname
import resource
import uiautomator2 as u2
import time
import random

trade_account = ""
trade_pwd = ""

trade_buy_page_xpath = '//*[@resource-id="com.lphtsccft:id/trade_function_recycler"]/android.view.ViewGroup[1]/android.view.View[1]'
trade_sell_page_xpath = '//*[@resource-id="com.lphtsccft:id/trade_function_recycler"]/android.view.ViewGroup[2]/android.view.View[1]'
trade_refund_page_xpath = '//*[@resource-id="com.lphtsccft:id/trade_function_recycler"]/android.view.ViewGroup[3]/android.view.View[1]'

# d(resourceId="com.lphtsccft:id/trade_normal_editLayout")
trade_buy_code_xpath = '//*[@resource-id="com.lphtsccft:id/trade_normal_editLayout"]' 

# //*[@text="买入价格"]
# rect {"x":95,"y":468,"width":574,"height":116}
# d(resourceId="com.lphtsccft:id/et_content", text="买入价格")
# d.click(0.333, 0.246)
trade_buy_price_xpath = '//*[@resource-id="com.lphtsccft:id/et_content"]' 
trade_buy_price_xpath = '//*[@resource-id="com.lphtsccft:id/main_layout"]/android.widget.EditText[1]'

# //*[@text="买入数量"]
# rect 	{"x":95,"y":649,"width":574,"height":116}
# d(resourceId="com.lphtsccft:id/et_content", text="买入数量")
# d.click(0.338, 0.324)
trade_buy_amount_xpath = '//*[@resource-id="com.lphtsccft:id/et_content"]' 
trade_buy_amount_xpath = '//*[@resource-id="com.lphtsccft:id/main_layout"]/android.widget.EditText[2]'

# 点击买入
trade_buy_action_xpath = '//*[@resource-id="com.lphtsccft:id/tv_trade"]'

# d(resourceId="com.lphtsccft:id/trade_normal_editLayout")
trade_sell_code_xpath = '//*[@resource-id="com.lphtsccft:id/trade_normal_editLayout"]' 

# //*[@text="卖出价格"]
# rect {"x":95,"y":468,"width":574,"height":116}
# d(resourceId="com.lphtsccft:id/et_content", text="卖出价格")
# d.click(0.333, 0.246)
trade_sell_price_xpath = '//*[@resource-id="com.lphtsccft:id/et_content"]'
trade_sell_price_xpath = '//*[@resource-id="com.lphtsccft:id/main_layout"]/android.widget.EditText[1]' 

# //*[@text="卖出数量"]
# rect 	{"x":95,"y":649,"width":574,"height":116}
# d(resourceId="com.lphtsccft:id/et_content", text="卖出数量")
# d.click(0.338, 0.324)
trade_sell_amount_xpath = '//*[@resource-id="com.lphtsccft:id/et_content"]' 
trade_sell_amount_xpath = '//*[@resource-id="com.lphtsccft:id/main_layout"]/android.widget.EditText[2]'

trade_sell_action_xpath = '//*[@resource-id="com.lphtsccft:id/tv_trade"]'

# 连接设备
d = u2.connect("c4fac50e") 


def login_and_open_trade_page(trade_buy_page_xpath, d):
    """登录打开交易"""
    d.app_stop("com.lphtsccft")
    time.sleep(1)

# 点击 Home 键
# 打开 app
    d(resourceId="com.android.systemui:id/home").click()
    d.app_start("com.lphtsccft")
    time.sleep(1)

# 在桌面打开 app 列表
# d(resourceId="com.android.systemui:id/home").click()
# d(resourceId="net.oneplus.launcher:id/all_apps_handle").click()

# 打开张乐财富通
# d(resourceId="net.oneplus.launcher:id/icon", text="涨乐财富通").click()

# 点击打开账户
    d.xpath('//*[@resource-id="com.lphtsccft:id/ll_animator_container"]/android.widget.ViewAnimator[5]/android.widget.ImageView[1]').click()
    time.sleep(1)

# 点击密码输入框
    d(resourceId="com.lphtsccft:id/login_password_edit").click()

# 输入密码
    d.send_keys(trade_pwd, clear=True)

# 点击登录
    d(resourceId="com.lphtsccft:id/login_ll_login").click()

# 点击 首页 -》 交易 tab
    d.xpath('//*[@resource-id="com.lphtsccft:id/ll_animator_container"]/android.widget.ViewAnimator[3]/android.widget.ImageView[1]').click()
    time.sleep(1)

# 交易 买入
    d.xpath(trade_buy_page_xpath).click()


def buy_v1(code, price, amount):
    d.xpath(trade_buy_code_xpath).click()
    d.send_keys(code, clear=True)
    # d(focused=True).set_text(code)
    # d(resourceId="com.lphtsccft:id/trade_normal_editLayout").child_by_instance(className="android.widget.EditText",inst=0).set_text(code)
    # d(resourceId="com.lphtsccft:id/trade_normal_editLayout").send_keys(code)

    d.xpath(trade_buy_price_xpath).click()
    d.send_keys(f'{price}', clear=True)
    # d(resourceId="com.lphtsccft:id/main_layout").child_by_instance(resourceId="com.lphtsccft:id/et_content",inst=0).set_text(f'{price}')
    # d(focused=True).set_text(f'{price}')

    d.xpath(trade_buy_amount_xpath).click()
    d.send_keys(f'{amount}', clear=True)
    # d(focused=True).set_text(f'{amount}')
    # d(resourceId="com.lphtsccft:id/main_layout").child_by_instance(resourceId="com.lphtsccft:id/et_content",inst=1).set_text(f'{amount}')
    d(resourceId="com.lphtsccft:id/tv_trade").click()

    # d(resourceid="com.lphtsccft:id/dialog_btn_left").click()
    # d(resourceid="com.lphtsccft:id/dialog_btn_right").click()
    d(text="确定").click()
    d(text="确定").click_exists(timeout=1)
    # d(text="取消").click()
    # d(text="取消").click_exists(timeout=1)

def buy(code, price, amount):
    d(resourceId="com.lphtsccft:id/title_container").child_by_instance(className="android.widget.TextView",inst=0).click()
    # 输入 code
    # d.xpath(trade_buy_code_xpath).click()
    d(resourceId="com.lphtsccft:id/trade_normal_editLayout").click_exists(timeout=0.5)
    d.send_keys(code, clear=True)
    # 输入 price
    d(resourceId="com.lphtsccft:id/main_layout").child_by_instance(resourceId="com.lphtsccft:id/et_content",inst=0).set_text(f'{price}')
    # 输入 amount
    d(resourceId="com.lphtsccft:id/main_layout").child_by_instance(resourceId="com.lphtsccft:id/et_content",inst=1).set_text(f'{amount}')
    # 点击 买入
    d(resourceId="com.lphtsccft:id/tv_trade").click()
    # 点击 确认矿 确定
    d(text="确定").click()
    # 点击 提示矿 确定（存在时）
    d(text="确定").click_exists(timeout=1)
    # d(text="取消").click()
    # d(text="取消").click_exists(timeout=1)

def sellV1(code, price, amount):
    d.xpath(trade_sell_code_xpath).click()
    d.send_keys(code, clear=True)
    d.xpath(trade_sell_price_xpath).click()
    d.send_keys(f'{price}', clear=True)
    d.xpath(trade_sell_amount_xpath).click()
    d.send_keys(f'{amount}', clear=True)

def sell(code, price, amount):
     # 输入 code
    d(resourceId="com.lphtsccft:id/title_container").child_by_instance(className="android.widget.TextView",inst=1).click()
    # d.xpath(trade_sell_code_xpath).click()
    d(resourceId="com.lphtsccft:id/trade_normal_editLayout").click_exists(timeout=0.5)
    d.send_keys(code, clear=True)
    # 输入 price
    d(resourceId="com.lphtsccft:id/main_layout").child_by_instance(resourceId="com.lphtsccft:id/et_content",inst=0).set_text(f'{price}')
    # 输入 amount
    d(resourceId="com.lphtsccft:id/main_layout").child_by_instance(resourceId="com.lphtsccft:id/et_content",inst=1).set_text(f'{amount}')
    # 点击 卖出
    d(resourceId="com.lphtsccft:id/tv_trade").click()
    # 点击 确认矿 确定
    d(text="确定").click()
    # 点击 提示矿 确定（存在时）
    d(text="确定").click_exists(timeout=1)
    # d(text="取消").click()
    # d(text="取消").click_exists(timeout=1)

login_and_open_trade_page(trade_buy_page_xpath, d)

buy(code= "000625", price="12.34", amount= 100)
# sell(code= "000625", price="12.34", amount= 100)


