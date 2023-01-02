#!/usr/bin/env python
# coding: utf-8

# In[1]:


import backtrader as bt
import datetime
import pandas as pd


# In[7]:


# Create a Stratey
class ToyStrategy(bt.Strategy):
    '''
    Empty strategy is used to study indicators
    '''
    params = (
        ('none', 0),
    )
    
    def log(self, txt):
        ''' Logging function for this strategy'''
        dt = self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def __init__(self):
        #bt.talib.KAMA(self.data0.close, timeperiod=3)
        pass
    
    def prenext(self):
        #self.log('prenext:{}-{}'.format(self.data0.close[0],self.data0.open[0]))
        pass
        
    def next(self):
        self.log('next:{}-{}'.format(self.data0.close[0], len(self)))
        l = len(self)
        
        if 1==l:
            self.log('buy1')
            self.buy(size=1)
        elif 2==l:
            self.log('sell2')
            self.sell(size=2)
        elif 3==l:
            self.log('close')
            self.close()
        elif 4==l:
            self.log('close')
            self.close()
    
    def stop(self):
        pass


# In[8]:


cerebro = bt.Cerebro(oldtrades=False, stdstats=False)

from simplelivingfeed import SimpleLivingData
from autoguibroker import AutoGuiBroker

feed = SimpleLivingData('ixic', timeframe=bt.TimeFrame.Seconds, compression=30)
cerebro.adddata(feed, name='simple living')
#cerebro.resampledata(feed, name='cy_weekly', timeframe=bt.TimeFrame.Minutes, compression=1)

cerebro.addstrategy(ToyStrategy)

cerebro.broker = AutoGuiBroker()

# init cash
cerebro.broker.setcash(10000.0)

print('Starting Running')

result = cerebro.run()

print('Finish Running')

