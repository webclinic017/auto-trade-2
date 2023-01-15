import datetime
import pandas_ta as ta
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover, resample_apply
from backtesting.test import GOOG

class RsiOscillator(Strategy):

    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    position_size = 0.1

    # Do as much initial computation as possible
    def init(self):
        self.daily_rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)
        
        # self.weekly_rsi = resample_apply(
        #     "W-FRI", ta.rsi, self.data.Close, self.rsi_window)

    # Step through bars one by one
    # Note that multiple buys are a thing here
    def next(self):
        price = self.data.Close[-1]

        if (crossover(self.daily_rsi, self.upper_bound)):
            self.position.close()

        # elif (crossover(self.lower_bound, self.daily_rsi)):
        elif (self.lower_bound > self.daily_rsi[-1]):
            self.buy(size=self.position_size) #size：仓位大小

bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)

stats = bt.run()

print(stats)

bt.plot()