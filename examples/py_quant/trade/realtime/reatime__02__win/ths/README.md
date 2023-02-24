
## ThsTrader

### 介绍
一个极简同花顺自动下单库，使用pyautogui实现。

### 软件架构
提供ThsTrader类，来完成程序化下单。支持量化交易。

### 版本信息
1. 20200628日上传初版（实现买，卖，得到持仓功能）
2. 20200629因网友要求，增加自动将下单程序放到前台。调用每个函数时会先将界面置顶。

### 安装教程
将 trader_ths.py 和 thstoken.png复制到自己的工程代码目录即可

### 使用说明
1. 安装 pyautogui： pip install pyautogui

2. 导入 ThsTrader 类： form trader_ths import ThsTrader

3. 测试代码：

trader=ThsTrader()
while trader.InitThs()!=True:
print("没有发现下单程序！")
trader.GetHold()
trader.RunBuy("000001",'12.55','100')
trader.RunSell("000001",'12.55','100')

4. 第一次运行代码有可能找不到下单程序。将InitThs函数中第一行取消注释，运行一次即可。

记住两点：
  1. 运行代码前要先将下单程序移动到左上角位置。具体说明可参考getmousepos.py代码中说明。
  2. 运行完第一次后，一定要将这行代码注释掉。
     #im = pyautogui.screenshot('thstoken.png',region=(0,0, 150, 200))