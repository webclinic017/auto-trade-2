import datetime

import backtrader as bt
import pandas as pd

import stock_db as sdb


class MultiTestStrategy(bt.Strategy):
    params = (
        ('maperiod', 20),
    )

    def prenext(self):
        pass

    def downcast(self, amount, lot):
        return abs(amount // lot * lot)

    def __init__(self):
        # 初始化交易指令
        self.order = None
        self.buy_list = []
        # 添加移动平均线指标，循环计算每个股票的指标
        self.sma = {x: bt.ind.SMA(self.getdatabyname(x), period=self.p.maperiod) for x in self.getdatanames()}

    def next(self):
        if self.order:  # 检查是否有指令等待执行
            return
        # 如果是最后一天，不进行买卖
        if pd.Timestamp(self.datas[0].datetime.date(0)) == end_dates[self.datas[0]._name]:
            return
        # 是否持仓
        if len(self.buy_list) < 2:  # 没有持仓
            # 没有购买的票
            for secu in set(self.getdatanames()) - set(self.buy_list):
                data = self.getdatabyname(secu)
                # 如果突破 20 日均线买买买，不要在最后一根bar的前一天买
                if data.close > self.sma[secu] and pd.Timestamp(data.datetime.date(1)) < end_dates[secu]:
                    # 买买买
                    order_value = self.broker.getvalue() * 0.48
                    order_amount = self.downcast(order_value / data.close[0], 100)
                    self.order = self.buy(data, size=order_amount, name=secu)
                    self.log(f"买{secu}, price:{data.close[0]:.2f}, amout: {order_amount}")
                    self.buy_list.append(secu)
        elif self.position:
            now_lst = []
            for secu in self.buy_list:
                data = self.getdatabyname(secu)
                # 执行卖出条件判断：收盘价格跌破20日均线，或者股票最后一根bar 的前一天之剔除日
                if data.close[0] < self.sma[secu] or pd.Timestamp(data.datetime.date(1)) >= end_dates[secu]:
                    # 卖卖卖
                    self.order = self.order_target_percent(data, 0, name=secu)
                    self.log(f"卖{secu}, price:{data.close[0]:.2f}, pct: 0")
                    continue
                now_lst.append(secu)
            self.buy_list = now_lst

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(f"""买入{order.info['name']}, 成交量{order.executed.size}，成交价{order.executed.price:.2f}""")
                self.log(
                    f'资产：{self.broker.getvalue():.2f} 持仓：{[(x, self.getpositionbyname(x).size) for x in self.buy_list]}')
            elif order.issell():
                self.log(f"""卖出{order.info['name']}, 成交量{order.executed.size}，成交价{order.executed.price:.2f}""")
                self.log(
                    f'资产：{self.broker.getvalue():.2f} 持仓：{[(x, self.getpositionbyname(x).size) for x in self.buy_list]}')
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


# 开始查询时间
start_query = '2019-01-01'
end_query = '2022-09-01'

# 开始回测时间
from_date = datetime.datetime(2022, 1, 1)
to_date = datetime.datetime(2022, 10, 10)
cerebro = bt.Cerebro()
# 添加几个股票数据
codes = [
    '300015',
    '300347',
    '300760',
    '603127',
    '600438'
]

# 添加多个股票回测数据
end_dates = {}
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
    end_dates[code] = data.index[-1]  # 股票剔除日
    end_date = data.index[-1]  # 股票剔除日
    print('添加股票数据：code: %s' % code)

cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)
cerebro.addstrategy(MultiTestStrategy, maperiod=20)
cerebro.run()
# 获取回测结束后的总资金
portvalue = cerebro.broker.getvalue()
# 打印结果
print(f'结束资金: {round(portvalue, 2)}')
cerebro.plot()

if __name__ == '__main__':
    pass