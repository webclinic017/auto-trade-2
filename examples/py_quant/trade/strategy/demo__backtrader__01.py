from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import pandas as pd
import datetime
from matplotlib import pyplot as plt
# %matplotlib inline

from backtesting.test import GOOG

class MyStrategy(bt.Strategy):
    
    #设定全局交易策略参数，这里默认SMA的period为20
    params = (('period', 20),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data, period=self.params.period)

    def prenext(self):
        return self.next()

    def next(self):
        # 如果Close值大于均值，则做多
        if self.sma < self.data.close:
            submitted_order = self.buy()
        # 如果Close值小于均值，则做空
        elif self.sma > self.data.close:
            submitted_order = self.sell()

    def start(self):
        print('回测准备启动')

    def stop(self):
        print('回测已经结束')

    def notify_order(self, order):
        print('收到一个Order')

# df = pd.read_csv('AAPL_20211216.csv')
# df['datetime'] = pd.to_datetime(df['Date'])
# df.set_index('datetime', inplace=True)

df = GOOG
df.reset_index(inplace=True, drop=False)
print(df)
df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume'];
df['datetime'] = pd.to_datetime(df['datetime'].values)
df.index = pd.to_datetime(df.index.values)
df = df.set_index('datetime')
# data.reset_index(inplace=True, drop=False)
print(df.columns)
print(df)

start_date = datetime.datetime(2004,8,19)
end_date = datetime.datetime(2013,3,1)

data  = bt.feeds.PandasData(dataname = df,
                                fromdate = start_date,
                                todate = end_date)

cerebro = bt.Cerebro()

cerebro.adddata(data) 

cerebro.addstrategy(MyStrategy)

cerebro.broker.setcash(10000) 
cerebro.broker.setcommission(commission=0.002)

cerebro.run()
cerebro.plot()

print(f'初始资金：{round(10000,2)}')
print(f"回测时间：{start_date.strftime('%Y-%m-%d')}:{end_date.strftime('%Y-%m-%d')}")
print(f'最终资金：{round(cerebro.broker.getvalue(),2)}')
print(f'最终收益：{round(cerebro.broker.getvalue() - 10000,2)}')
print(f'收益率：{round((cerebro.broker.getvalue() - 10000)/10000,4)}')