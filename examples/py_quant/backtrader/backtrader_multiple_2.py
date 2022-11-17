"""A Simple Strategy Trading Two Stocks
Original code: https://blog.csdn.net/qq_26948675/article/details/80016633
Modified based on: https://www.backtrader.com/blog/posts/2018-04-22-improving-code/improving-code.html
Replaced the local CSV files with online data from IEX.
Unfortunately, this strategy is not profitable for the two stocks picked.
"""

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import pandas as pd
# Import the backtrader platform
import backtrader as bt

import akshare as ak  # 升级到最新版

# Data Source
import pandas_datareader.data as web
# To avoid downloading the same data more than once
import joblib

joblib_cache_dir = "./build/cache/"
if not os.path.exists(joblib_cache_dir):
        os.makedirs(joblib_cache_dir)

MEMORY = joblib.Memory(cachedir= joblib_cache_dir)

"""
import joblib
# joblib 是一组在 Python 中提供轻量级管道的工具，
# 在处理大数据时速度更快、更健壮，
# 并且对numpy数组进行了特定的优化。
# 所以在保存速度上，较之pickle和dill，joblib速度更快。
# 保存模型
def save_model(model, filename):
	# 后缀一般用pkl
	joblib.dump(model, filename=filename)
	
# 加载模型
def load_model(filename):
	model = joblib.load(filename)
	return model

import pickle
# pickle 基于二进制协议，将 Python 对象结构进行序列化与反序列化。
# dump 保存对应序列化 picking 过程，将 Python 对象层级结构转换为字节流的过程。
# load 加载对应 unpicking 逆运算过程，将字节流转换回对象层级结构的过程。
# 保存模型
def save_model(model, filePath):
	# 路径需要预先建立好
	with open(filePath, 'wb') as f:
		pickle.dump(model, f)

# 加载模型
def load_model(filePath):
	with open(filePath, 'rb') as f:
		model = pickle.load(f)
	return model

import dill
# dill 原理与 pickle 一致，
# 但是区别在于 dill 可以对自定义的模型进行保存与加载，
# 而pickle不行。
# 保存模型
def save_model(model, filePath):
	# 路径需要预先建立好
	with open(filePath, 'wb') as f:
		dill.dump(model, f)

# 加载模型
def load_model(filePath):
	with open(filePath, 'rb') as f:
		model = dill.load(f)
	return model
"""

# @MEMORY.cache
# def get_data(symbol, start, end):
#     df_prices = web.DataReader(
#         symbol, 
#         'iex',
#         start, end).reset_index()
#     df_prices["date"] = pd.to_datetime(df_prices.date)
#     return df_prices.set_index("date")

symbel_list = [
    # "600519", 
    "000858", 
    "300750",
]

@MEMORY.cache
def get_data(symbol, start, end):
    # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
    df_prices = ak.stock_zh_a_hist(symbol=symbol, adjust="hfq", start_date= start, end_date=end).iloc[:, :6]
    # 处理字段命名，以符合 Backtrader 的要求
    df_prices.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
    ]
    # 把 date 作为日期索引，以符合 Backtrader 的要求
    # df_prices.index = pd.to_datetime(df_prices['date'])
    df_prices["date"] = pd.to_datetime(df_prices['date'])
    df_prices = df_prices.set_index("date")
    print(df_prices.head(5))
    print(df_prices.tail(5))
    return df_prices


class TestStrategy(bt.Strategy):
    params = (
        # Standard MACD Parameters
        ('period_m', 13),
        ('period', 5),
        ('prepend_constant', True),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose_x = self.datas[0].close
        self.dataclose_y = self.datas[1].close
        m = self.dataclose_x

        ma1 = bt.indicators.SMA(
            self.data0, period=self.p.period)
        ma2 = bt.indicators.SMA(
            self.data1, period=self.p.period)
        # Use a built-in indicator
        ma1_pct = bt.ind.PctChange(ma1, period=1)  # The ma1 percentage part
        ma2_pct = bt.ind.PctChange(ma2, period=1)  # The ma2 percentage part
        # # Use line delay notation (-x) to get a ref to the -1 point
        # ma1_pct = ma1 / ma1(-1) - 1.0  # The ma1 percentage part
        # ma2_pct = ma2 / ma2(-1) - 1.0  # The ma2 percentage part

        m1_pct_ = bt.ind.PctChange(self.dataclose_x, period=self.params.period_m)
        m2_pct_ = bt.ind.PctChange(self.dataclose_y, period=self.params.period_m)

        self.buy_sig = ma1_pct > ma2_pct  # buy signal
        self.sell_sig = ma1_pct <= ma2_pct  # sell signal

        self.buy_sig = m1_pct_ > m2_pct_ # and self.dataclose_x > ma1 # buy signal
        self.sell_sig = m1_pct_ <= m2_pct_ #  or self.dataclose_x <= ma1 # sell signal

        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_cashvalue(self, cash, value):
        self.log('Cash %s Value %s' % (cash, value))

    def notify_order(self, order):
        print(type(order), 'Is Buy ', order.isbuy())
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def prenext(self):
        print('prenext:: current:', self)
        self.next()

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose_x[0])
        self.log('Close, %.2f' % self.dataclose_y[0])
        # Check if we are in the market
        if not self.getposition(self.datas[1]):
            # Not yet ... we MIGHT BUY if ...
            if self.buy_sig:
                    # if sma[0]<top[-5]:
                # BUY, BUY, BUY!!! (with default parameters)
                self.log('BUY CREATE,{},{}'.format(
                    self.dataclose_y[0], self.dataclose_x[0]))
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy(self.datas[0])
                self.order = self.sell(self.datas[1])

        else:
            # Already in the market ... we might sell
            if self.sell_sig:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('BUY CREATE,{},{}'.format(
                    self.dataclose_y[0], self.dataclose_x[0]))
                # Keep track of the created order to avoid a 2nd order
                self.log('Pos size %s' % self.position.size)
                self.order = self.close(self.datas[1])
                self.order = self.close(self.datas[0])

def bar_size(df, fromdate, todate):
    return len(df[(df['date'] >= fromdate.strftime('%Y-%m-%d')) 
            & (df['date'] <= todate.strftime('%Y-%m-%d'))])

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    # Create a Data Feed
    start_date = datetime.datetime(2018, 10, 8)
    end_date = datetime.datetime(2022, 11, 11)

    df_list = [get_data(
        symbel,  
        start_date.strftime('%Y%m%d'),
        end_date.strftime('%Y%m%d'),
    ) for symbel in symbel_list]

    bar_size_list = [len(df) for df in df_list]

    print(f'bar_size_list: {bar_size_list}')

    data_list = [bt.feeds.PandasData(
        dataname=df,
        openinterest=-1,
        # reversed=False,
        timeframe=bt.TimeFrame.Days,
        fromdate=start_date, 
        todate=end_date,
    ) for df in df_list]
    print(f'size data_list: {len(data_list)}')

    for data in data_list:
        cerebro.adddata(data=data)

    # df0 = get_data(
    #     symbel_list[0], 
    #     start_date.strftime('%Y%m%d'),
    #     end_date.strftime('%Y%m%d')
    # )
    # df1 = get_data(
    #     symbel_list[0], 
    #     start_date.strftime('%Y%m%d'),
    #     end_date.strftime('%Y%m%d')
    # )
    # data_1 = bt.feeds.PandasData(
    #     dataname=get_data(
    #         symbel_list[0], 
    #         start_date.strftime('%Y%m%d'),
    #         end_date.strftime('%Y%m%d')),
    #     fromdate=start_date, 
    #     todate=end_date,
    # )
    # data_2 = bt.feeds.PandasData(
    #     dataname=get_data(
    #         symbel_list[1], 
    #         start_date.strftime('%Y%m%d'),
    #         end_date.strftime('%Y%m%d')),
    #     fromdate=start_date,
    #     todate=end_date,
    # )

    # # Add the Data Feed to Cerebro
    # cerebro.adddata(data_1, start_date)
    # cerebro.adddata(data_2)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()