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

    # Do as much initial computation as possible
    def init(self):
        self.daily_rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)
        
        # self.weekly_rsi = resample_apply(
        #     "W-FRI", ta.rsi, self.data.Close, self.rsi_window)

    # Step through bars one by one
    # Note that multiple buys are a thing here
    def next(self):
        if (crossover(self.daily_rsi, self.upper_bound)):
            if self.position.is_long:
                print(f'size: {self.position.size} pl_pct: {self.position.pl_pct}')
                self.position.close()   
                self.sell() # short 做空

        elif (crossover(self.lower_bound, self.daily_rsi)):
            if self.position.is_short or not self.position:
                self.position.close()
                self.buy() # long 做多

bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)

stats = bt.run()

print(stats)

bt.plot()