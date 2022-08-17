# Python 移动端自动化

## 工作原理：

python-uiautomator2 主要分为两个部分，python 客户端，移动设备

python 端: 运行脚本，并向移动设备发送 HTTP 请求；
移动设备：移动设备上运行了封装了 uiautomator2 的 HTTP 服务，解析收到的请求，并转化成 uiautomator2 的代码；
整个过程：

在移动设备上安装 atx-agent(守护进程)，随后 atx-agent 启动 uiautomator2 服务(默认 7912 端口)进行监听；
在 PC 上编写测试脚本并执行（相当于发送 HTTP 请求到移动设备的 server 端）；
移动设备通过 WIFI 或 USB 接收到 PC 上发来的 HTTP 请求，执行制定的操作。

## 环境

一台电脑，这里用的 Mac，安装 Anaconda，

一台手机，这里用的 OnePlus 5T

```bash
pip3 install uiautomator2

pipe install weditor
```

测试 uiautomator2 是否安装成功 

```python 
# 测试 uiautomator2 是否安装成功
import uiautomator2 as u2
device = u2.connect()

```

打开 weditor

```bash
weditor
# python3 -m weditor
```

输入 Device alias，点击 Connect 连接

实时开关打开

## 自动化案例 自动化玩腾讯微证券领长牛 python 实现

需要先关注腾讯自选股微信版|微证券公众号。

```python
import uiautomator2 as u2
import time
import random

def automatic_click(device, times):
    for i in range(20):
        x = random.randint(388, 677)  # X坐标范围
        y = random.randint(1000, 1200)  # Y坐标范围
        device.long_click(x, y, 0.01)
        time.sleep(0.01)

    time.sleep(0.01)
    device.click(1002, 1081)
    device.click(1002, 1081)
    print("第%d次自动化操作结束" % times)


device = u2.connect_wifi("192.168.95.139")  # 跟上图中的IP地址是对应的

print("打开微信")
device.app_start("com.tencent.mm")
time.sleep(2) ## 休眠2s等待微信
device(resourceId="com.tencent.mm:id/he6").click()  # 点击搜索
device.send_keys("腾讯自选股微信版")  
device(text="腾讯自选股微信版|微证券").click()
device(resourceId="com.tencent.mm:id/av9", text="🔥好福利").click()
device.xpath('//*[@text="🐮领长牛！"]').click()
time.sleep(3)


for i in range(100):
    automatic_click(device, i+1)
device.service("uiautomator").stop()  # 此语句根据情况进行添加或者删除
print("任务结束")
```

## 账户登录

```python
import uiautomator2 as u2
import time
import random

# 连接设备
d = u2.connect("c4fac50e") 

d.app_start("com.lphtsccft")

# 在桌面打开 app 列表
d(resourceId="com.android.systemui:id/home").click()
d(resourceId="net.oneplus.launcher:id/all_apps_handle").click()

# 打开张乐财富通
d(resourceId="net.oneplus.launcher:id/icon", text="涨乐财富通").click()

# 点击打开账户
d.xpath('//*[@resource-id="com.lphtsccft:id/ll_animator_container"]/android.widget.ViewAnimator[5]/android.widget.ImageView[1]').click()

# 点击密码输入框
d(resourceId="com.lphtsccft:id/login_password_edit").click()
# 输入密码
d.send_keys("", clear=True)

# 点击登录
d(resourceId="com.lphtsccft:id/login_ll_login").click()
```

