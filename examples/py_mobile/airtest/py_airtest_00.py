# -*- encoding=utf8 -*-
__author__ = "afirez"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/c4fac50e?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH",])

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# script content
print("start...")

keyevent("HOME")
keyevent("BACK")

start_app("com.lphtsccft")
sleep(2.0)
# touch(Template(r"tpl1667365479453.png", record_pos=(0.363, 0.812), resolution=(1080, 2160)))

poco(text="账户").wait_for_appearance()
if poco(text="账户").exists():
    poco(text="账户").click()

pwd = poco("com.lphtsccft:id/credit_dongtai_pwd").get_text()

print(f"pwd {pwd}")
# pwd = poco("请输入交易密码").get_text()
## 
# XPathLite //*[@resource-id="com.lphtsccft:id/login_password_edit"]


poco("com.lphtsccft:id/login_password_edit").click()

poco("com.lphtsccft:id/login_password_edit").set_text("123456")

pwd = poco("com.lphtsccft:id/login_password_edit").get_text()

print(f"pwd {pwd}")

poco("com.lphtsccft:id/login_ll_login").click()
sleep(2.0)

# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)