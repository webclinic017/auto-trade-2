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


# device = u2.connect_wifi("192.168.95.139")  # 跟上图中的IP地址是对应的
device = u2.connect("c4fac50e")  # 跟上图中的IP地址是对应的

print("打开微信")
device.app_start("com.tencent.mm")
time.sleep(2) ## 休眠2s等待微信
device(resourceId="com.tencent.mm:id/j5t").click()  # 点击搜索
device.send_keys("腾讯自选股微信版")  
device(text="腾讯自选股微信版微证券").click()
time.sleep(1)
device(text="腾讯自选股微信版|微证券").click()
device(resourceId="com.tencent.mm:id/av9", text="🔥好福利").click()
device.xpath('//*[@text="🐮领长牛！"]').click()
time.sleep(3)


for i in range(100):
    automatic_click(device, i+1)
device.service("uiautomator").stop()  # 此语句根据情况进行添加或者删除
print("任务结束")

