#交易策略为连续下跌3天买入，连续上涨3天卖出
import pandas as pd
import matplotlib.pyplot as plt
import backtrader as bt
import backtrader.feeds as btfeed
import backtrader.indicators as btind
from backtrader import analyzers
import pyalgotrade
import  PySimpleGUI as sg
import akshare as ak
import pandas as pd
import datetime

stock=sg.popup_get_file('输入股票代码比如sz002466')
start_date=sg.popup_get_file('输入数据开始时间比如20200101')
start_cash=sg.popup_get_file('输入开始资金比如1000000')

#定义测试类
class testStrategy(bt.Strategy):
    #定义记录函数
    def log(self,txt,dt=None):
        dt=dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    #初始化数据
    def __init__(self):
        self.dataclose=self.datas[0].close
    #定义交易状态检测函数，交易前
    def notify_order(self,order):
        #如果交易提交/接受
        if order.status in [order.Submitted,order.Accepted]:
            print('交易提交，交易接受')
        #如果交易完成
        if order.status in [order.Completed]:
            #如果交易类型是买
            if order.isbuy():
                self.log('买的价格:%.2f,交易成本: %.2f,交易佣金: %.2f' % 
                (order.executed.price,order.executed.value,order.executed.comm))
                self.buyprice=order.executed.price
                self.buycomm=order.executed.comm
            #如果交易类型是卖
            elif order.issell():
                self.log('卖的价格:%.2f,交易收益: %.2f,交易佣金: %.2f' % 
                (order.executed.price,order.executed.value,order.executed.comm))
                self.buyprice=order.executed.price
                self.buycomm=order.executed.comm
            self.bar_executed=len(self)
        #如果交易交易取消，保证金不足，交易拒绝
        elif order.status in [order.Canceled,order.Margin,order.Rejected]:
          self.log('交易取消/保证金不足/交易拒绝')  
        self.order=None
    #交易完成后的函数
    def notify_trade(self,trade):
        #如果交易没有完成
        if not trade.isclosed:
            return '交易没有结束，等待结束'
        #交易完成
        self.log('利润 %.2f,总收入 %.2f' %(trade.pnl,trade.pnlcomm))
    #主交易函数
    def next(self):
        self.log('收盘价,%.2f' % self.dataclose[0])
        #检测交易是不是挂起
        #检测有没有在市场，在进行交易
        if not self.position:
            #写交易函数，连续下跌3天买入,连续上涨3天卖出
            #如果今天的价格小于昨天的价格
            if self.dataclose[0]<self.dataclose[-1]:
                #如果昨天的价格小于前天的价格
                if self.dataclose[-1]<self.dataclose[-2]:
                    #记录买卖的价格
                    self.log('买的价格 %.2f' % self.dataclose[0])
                    self.buy(size=200)#单位为股，代表1手
            elif self.dataclose[0]>self.dataclose[-1]:
                if self.dataclose[-1]>self.dataclose[-2]:
                    self.log('卖出的价格 %.2f' %self.dataclose[0])
                    self.sell(size=100)
        #如果已经加入市场
        else:
            if len(self)>=(self.bar_executed+5):
                self.log('卖的价格 %.2f' % self.dataclose[0])
                #保持创建，避免交易
                self.order=self.sell()
#简单例子
if __name__ == "__main__":
    #将大脑实例化
    cerebro=bt.Cerebro()
    cerebro.addstrategy(testStrategy)
    #加入数据
    df=ak.stock_zh_a_daily(symbol=stock,start_date=start_date)
    df.index=pd.to_datetime(df['date'])
    data=btfeed.PandasData(dataname=df)
    cerebro.adddata(data=data)
    #设置开始资金
    cerebro.broker.set_cash(int(start_cash))
    #设置交易费用
    cerebro.broker.setcommission(0.003)
    print('开始值{}'.format(cerebro.broker.getvalue()))
    cerebro.run()
    print('最终值{}'.format(cerebro.broker.getvalue()))
    cerebro.plot(style='candle')
    plt.show()