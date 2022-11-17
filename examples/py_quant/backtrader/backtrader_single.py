from time import time
from datetime import datetime
import backtrader as bt

class single_strategy(bt.Strategy):
    # 全局设定交易策略的参数
    params = (
        ('maperiod', 20),
    )

    def __init__(self):
        # 初始化交易指令
        self.order = None

        # 添加移动均线指标，内置了talib模块
        self.sma = bt.ind.SMA(self.datas[0], period=self.params.maperiod)

    # 可以不要，但如果你数据未对齐，需要在这里检验
    def prenext(self):
        pass
    
    def downcast(amount, lot):
        return abs(amount//lot*lot)
    
    
    def next(self):
        if self.order:  # 检查是否有指令等待执行,如果有就不执行这根bar
            return
        
        # 回测最后一天不进行买卖
        if self.datas[0].datetime.date(0) == end_date:
            return 
        
        # 拿这根bar时期的所有资产价值（如果按日K数据放入，即代表今日的资产价值）
        self.log("%.2f元" % self.broker.getvalue()) 
        if not self.position:  # 没有持仓
            
            # 执行买入条件判断：收盘价格上涨突破20日均线；
            # 不要在股票剔除日前一天进行买入
            if self.datas[0].close > self.sma and data.datetime.date(1) < end_date:
                # 永远不要满仓买入某只股票
                order_value = self.broker.getvalue()*0.98
                order_amount = downcast(order_value/self.datas[0].close[0], 100)
                self.order = self.buy(self.datas[0], size=order_amount, name=self.datas[0]._name)
                self.log(f"买{self.datas[0]._name}, price:{self.datas[0].close[0]:.2f}, amout: {order_amount}")
                # self.order = self.order_target_percent(self.datas[0], 0.98, name=self.datas[0]._name)
                # self.log(f"买{self.datas[0]._name}, price:{self.datas[0].close[0]:.2f}, pct: 0.98")
        else:
            
            # 执行卖出条件判断：收盘价格跌破20日均线，或者股票剔除
            if self.datas[0].close > self.sma or data.datetime.date(1) >= end_date:
                # 执行卖出
                self.order = self.order_target_percent(self.datas[0], 0, name=self.datas[0]._name)
                self.log(f"卖{self.datas[0]._name}, price:{self.datas[0].close[0]:.2f}, pct: 0")

    def log(self, txt, dt=None):
        ''' 输出日志'''
        dt = dt or self.datas[0].datetime.date(0) # 拿现在的日期
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


cerebro = bt.Cerebro()
cerebro.addstrategy(single_strategy)
secu_lst = {'600000': {'start': '2020-01-01', 'end': '2020-07-18'}}
df = GetKdatas(secu_lst).merge_period()['600000']
data = PandasData_Extend(dataname=df, fromdate=df.index[0], todate=df.index[-1])
cerebro.adddata(data, name='600000')
end_date = df.index[-1] # 股票剔除日

# 设置初始资本为1 million
startcash = 10**6
cerebro.broker.setcash(startcash)
print(f"初始资金{cerebro.broker.getvalue()}")
# 设置交易手续费
cerebro.broker.addcommissioninfo(CommInfoPro())
# 运行回测系统
cerebro.run()
# 获取回测结束后的总资金
portvalue = cerebro.broker.getvalue()
# 打印结果
print(f'结束资金: {round(portvalue, 2)}')