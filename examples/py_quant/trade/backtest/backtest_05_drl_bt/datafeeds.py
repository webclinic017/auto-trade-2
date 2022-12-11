import time

import pandas as pd

import backtrader as bt


class RealTimeData(bt.feed.DataBase):

    data_origin = None

    def data_generator(self):
        while True:
            ... # 定义一些随机假数据
            data = pd.DataFrame()
            yield data # 返回数据
            time.sleep(5) # 实时系统 定义为每5秒生成一条假数据

    def start(self):
        self.data_origin = self.data_genrator()

    def stop(self):
        ...
        pass

    def _load(self):
        try:
            data = next(self.data_origin)
        except StopIteration:
            # 停止迭代 证明数据已经停止生成
            return False
        
        dt, o, h, l, c, v, oi = data

        self.lines.datetime[0] = dt
        self.lines.open[0] = o # 设定该时间的开盘价
        self.lines.high[0] = h # 设定该时段的最高价位
        self.lines.low[0] = l # 设定该时段的最低价位
        self.lines.close[0] = c # 设定该时段的收盘价
        self.lines.volume[0] = v # 设定该时段成交量
        self.lines.openinterest[0] = oi # 该时段的持仓量

        return True