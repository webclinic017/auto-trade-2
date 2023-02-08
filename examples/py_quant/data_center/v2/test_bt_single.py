import datetime

import backtrader as bt
import pandas as pd

import stock_db as sdb


class SingleTestStrategy(bt.Strategy):
    params = (
        ('maperiod', 20),
    )

    def __init__(self):
        self.order = None
        self.sma = bt.ind.SMA(self.data, period=self.p.maperiod)
        pass

    def downcast(self, amount, lot):
        return abs(amount // lot * lot)

    # 可以不要，但如果你数据未对齐，需要在这里检验
    def prenext(self):
        print('prenext 执行 ', self.datetime.date(), self.getdatabyname('300015')._name
              , self.getdatabyname('300015').close[0])
        pass

    def next(self):
        # 检查是否有指令执行，如果有则不执行这bar
        if self.order:
            return
        # 回测如果是最后一天，则不进行买卖
        if pd.Timestamp(self.data.datetime.date(0)) == end_date:
            return
        if not self.position:  # 没有持仓
            # 执行买入条件判断：收盘价格上涨突破20日均线；
            # 不要在股票剔除日前一天进行买入
            if self.datas[0].close > self.sma and pd.Timestamp(self.data.datetime.date(1)) < end_date:
                # 永远不要满仓买入某只股票
                order_value = self.broker.getvalue() * 0.98
                order_amount = self.downcast(order_value / self.datas[0].close[0], 100)
                self.order = self.buy(self.datas[0], order_amount, name=self.datas[0]._name)

        else:
            # 执行卖出条件判断：收盘价格跌破20日均线，或者股票剔除
            if self.datas[0].close < self.sma or pd.Timestamp(self.data.datetime.date(1)) >= end_date:
                # 执行卖出
                self.order = self.order_target_percent(self.datas[0], 0, name=self.datas[0]._name)
                self.log(f'卖{self.datas[0]._name},price:{self.datas[0].close[0]:.2f},pct: 0')
        pass

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    f"买入{order.info['name']}, 成交量{order.executed.size}，成交价{order.executed.price:.2f} 订单状态：{order.status}")
                self.log('买入后当前资产：%.2f 元' % self.broker.getvalue())
            elif order.issell():
                self.log(
                    f"卖出{order.info['name']}, 成交量{order.executed.size}，成交价{order.executed.price:.2f} 订单状态：{order.status}")
                self.log('卖出后当前资产：%.2f 元' % self.broker.getvalue())
            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None

    def log(self, txt, dt=None):
        """
        输出日期
        :param txt:
        :param dt:
        :return:
        """
        dt = dt or self.datetime.date(0)  # 现在的日期
        print('%s , %s' % (dt.isoformat(), txt))

    pass

    def notify_trade(self, trade):
        '''可选，打印交易信息'''
        pass


# 开始查询时间
start_query = '2019-01-01'
end_query = '2023-02-08'

# 开始回测时间
from_date = datetime.datetime(2022, 1, 1)
to_date = datetime.datetime(2023, 2, 8)
cerebro = bt.Cerebro()
# 添加几个股票数据
codes = [
    '300015',
    # '300347',
    # '300760',
    # '603127',
    # '600438'
]

# 添加多个股票回测数据
end_date = 0
for code in codes:
    data = sdb.stock_daily(code, start_query, end_query)
    data.set_index(['date'], inplace=True)
    print(data)
    data.index.names = ['datetime']
    data_feed = bt.feeds.PandasData(dataname=data,
                                    fromdate=from_date,
                                    todate=to_date)
    cerebro.adddata(data_feed, name=code)
    end_date = data.index[-1]  # 股票剔除日
    print('添加股票数据：code: %s' % code)

cerebro.broker.setcash(100000000.0)
cerebro.broker.setcommission(commission=0.001)
cerebro.addstrategy(SingleTestStrategy, maperiod=20)
cerebro.run()
cerebro.plot()

if __name__ == '__main__':
    pass