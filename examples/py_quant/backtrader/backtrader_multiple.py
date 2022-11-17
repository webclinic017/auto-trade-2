from time import time
from datetime import datetime
import backtrader as bt


class multi_strategy(bt.Strategy):
    # 全局设定交易策略的参数
    params = (
        ('maperiod', 20),
    )

    def __init__(self):
        # 初始化交易指令
        self.order = None
        self.buy_lst = []

        # 添加移动均线指标，内置了talib模块
        # 循环计算每只股票的指标
        self.sma = {x: bt.ind.SMA(self.getdatabyname(x), period=self.p.maperiod) for x in self.getdatanames()}

    def prenext(self):
        pass
    
        
    def downcast(self, amount, lot):
        return abs(amount//lot*lot)
    
    
    def next(self):
        if self.order:  # 检查是否有指令等待执行,
            return

        # 回测最后一天不进行买卖
        if self.datas[0].datetime.date(0) == end_date:
            return 
        
        # 检查是否持仓
        self.log(f'{self.broker.getvalue():.2f}, {[(x, self.getpositionbyname(x).size) for x in self.buy_lst]}')
        if len(self.buy_lst) < 2:  # 没有持仓
            for secu in set(self.getdatanames()) - set(self.buy_lst):
                data = self.getdatabyname(secu)
                # 执行买入条件判断：收盘价格上涨突破20日均线
                # 不要在股票剔除日前一天进行买入
                if data.close > self.sma[secu] and \
                    data.datetime.date(1) < pd.Timestamp(secu_lst[secu]['end']):
                    # 执行买入
                    order_value = self.broker.getvalue()*0.48
                    order_amount = self.downcast(order_value/data.close[0], 100)
                    self.order = self.buy(data, size=order_amount, name=secu)
                    self.log(f"买{secu}, price:{data.close[0]:.2f}, amout: {order_amount}")
                    self.buy_lst.append(secu)
        elif self.position:
            now_lst = []
            for secu in self.buy_lst:
                data = self.getdatabyname(secu)
                # 执行卖出条件判断：收盘价格跌破20日均线，或者股票剔除
                if (data.close < self.sma[secu]) or \
                    (data.datetime.date(1) >= pd.Timestamp(secu_lst[secu]['end'])):
                    # 执行卖出
                    self.order = self.order_target_percent(data, 0, name=secu)
                    # 也可以用 self.sell(data, size = self.getposition(data).size)
                    # or self.sell(data, size = self.getpositionbyname(secu).size)
                    self.log(f"卖{secu}, price:{data.close[0]:.2f}, pct: 0")
                    continue
                now_lst.append(secu)
            self.buy_lst = now_lst.copy()

    def log(self, txt, dt=None):
        ''' 输出日志'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(f"""买入{order.info['name']}, 成交量{order.executed.size}，成交价{order.executed.price:.2f}""")
            elif order.issell():
                self.log(f"""卖出{order.info['name']}, 成交量{order.executed.size}，成交价{order.executed.price:.2f}""")
            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None

        
secu_lst = {'600000': {'start': '2020-01-01', 'end': '2021-07-20'},
            '000001': {'start': '2020-02-01', 'end': '2021-08-18'}}
# 拿对齐的数据
kdata = GetKdatas(secu_lst).merge_period()
kdata = dict(sorted(kdata.items()))

# 开始回测
cerebro = bt.Cerebro()
cerebro.addstrategy(multi_strategy)

for secu in kdata.keys():
    df = kdata[secu]
    data = PandasData_Extend(dataname=df, fromdate=df.index[0], todate=df.index[-1])
    cerebro.adddata(data, name=secu)
end_date = df.index[-1]

# 设置初始资本为1 million
startcash = 10**6
cerebro.broker.setcash(startcash)
print(f"初始资金{cerebro.broker.getvalue()}")
# 设置交易手续费
cerebro.broker.addcommissioninfo(CommInfoPro())

# 加入指标
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='_pyfolio')
# 运行回测系统
thestrats = cerebro.run()
# 获取回测结束后的总资金
portvalue = cerebro.broker.getvalue()
# 打印结果
print(f'结束资金: {round(portvalue, 2)}')