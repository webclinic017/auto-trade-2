import datetime

import backtrader as bt

import stock_db as sdb


class PandasData_more(bt.feeds.PandasData):
    lines = ('pe', 'pb',)  # 要添加的线
    # 设置 line 在数据源上的列位置
    params = (
        ('pe', -1),
        ('pb', -1),
    )


class My_PandasData(bt.feeds.PandasData):
    params = (
        ('fromdate', datetime.datetime(2019, 1, 2)),
        ('todate', datetime.datetime(2021, 1, 28)),
        ('nullvalue', 0.0),
        ('dtformat', ('%Y-%m-%d')),
        ('datetime', 0),
        ('time', -1),
        ('high', 3),
        ('low', 4),
        ('open', 2),
        ('close', 5),
        ('volume', 6),
        ('openinterest', -1)
    )


class TestStrategy(bt.Strategy):
    # 可选，设置回测的可变参数：如移动均线的周期
    # params = (
    #     (..., ...),  # 最后一个“,”最好别删！
    # )

    def log(self, txt, dt=None):
        """
        可选，构建策略打印日志的函数：可用于打印订单记录或交易记录等
        :param txt:
        :param dt:
        :return:
        """
        dt = dt or self.datas[0].datetime.date(0)
        print('%s,%s' % (dt.isoformat(), txt))

    def __init__(self):
        """
        必选，初始化属性、计算指标等
        """

        print(type(self.datas[0].lines.datetime[0]))
        print(type(self.datas[0].lines.volume[0]))
        self.count = 0
        print("------------- init 中的索引位置-------------")
        print('lines', self.data1.lines.getlinealiases())
        print('datas type', type(self.datas))
        print("0 索引：", 'datetime', self.datas[1].lines.datetime.date(0), 'close', self.data1.lines.close[0])
        print('-1 索引：', 'datetime', self.data1.lines.datetime.date(-1), 'close', self.data1.lines.close[-1])
        print('-2 索引：', 'datetime', self.data1.lines.datetime.date(-2), 'close', self.data1.lines.close[-2])
        print('1 索引： ', 'datetime', self.data1.lines.datetime.date(1), 'close', self.data1.lines.close[1])
        print('2 索引： ', 'datetime', self.data1.lines.datetime.date(2), 'close', self.data1.lines.close[2])
        print('从 0 开始往前取3天的收盘价：', self.data1.lines.close.get(ago=0, size=3))
        print("从-1开始往前取3天的收盘价：", self.data1.lines.close.get(ago=3, size=3))
        print("从-2开始往前取3天的收盘价：", self.data1.lines.close.get(ago=-2, size=3))
        print("回测的总长度：", self.data.buflen())
        pass

    def notify_order(self, order):
        """
        可选，打印订单信息
        :param order:
        :return:
        """
        pass

    def notify_trade(self, trade):
        """
        可选，打印交易信息
        :param trade:
        :return:
        """
        pass

    def next(self):
        """
        必选，编写交易策略逻辑
        :return:
        """
        print(f"------------- next 的第{self.count + 1}次循环 --------------")
        print('当前节点(今日): ', 'datetime', self.data1.lines.datetime.date(0), 'close', self.data1.lines.close[0])
        print("往前推1天（昨日）：", 'datetime', self.data1.lines.datetime.date(-1), 'close', self.data1.lines.close[-1])
        print("往前推2天（前日）", 'datetime', self.data1.lines.datetime.date(-2), 'close', self.data1.lines.close[-2])
        print("前日、昨日、今日的收盘价：", self.data1.lines.close.get(ago=0, size=3))
        # print("往后推1天（明日）：", 'datetime', self.data1.lines.datetime.date(1), 'close', self.data1.lines.close[1])
        # print("往后推2天（明后日）", 'datetime', self.data1.lines.datetime.date(2), 'close', self.data1.lines.close[2])
        print("已处理的数据点：", len(self.data))
        print("回测的总长度：", self.data.buflen())
        self.count += 1
        pass


# 股票查询开始和结束时间
start_query = '2022-01-01'
end_query = '2022-09-01'
# 回测开始和结束时间
start_date = datetime.datetime(2022, 7, 11)
end_date = datetime.datetime(2022, 8, 10)
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
for code in codes:
    data = sdb.stock_daily(code, start_query, end_query)
    data.index.names = ['datetime']
    # 新增指标列
    data['pe'] = 3
    data['pb'] = 4
    date_feed = PandasData_more(dataname=data, fromdate=start_date, todate=end_date)
    cerebro.adddata(date_feed, name=code)
    print('添加股票数据：code: %s' % code)

cerebro.addstrategy(TestStrategy)
cerebro.run()
# cerebro.plot()

if __name__ == '__main__':
    pass