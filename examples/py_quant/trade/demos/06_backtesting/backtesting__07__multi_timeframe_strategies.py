import pandas_ta as ta
import pandas as pd

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
        
        self.weekly_rsi = resample_apply(
            "W-FRI", ta.rsi, self.data.Close, self.rsi_window)

    # Step through bars one by one
    # Note that multiple buys are a thing here
    def next(self):

        if (crossover(self.daily_rsi, self.upper_bound)
                and self.weekly_rsi[-1] > self.upper_bound):
            self.position.close()

        elif (crossover(self.lower_bound, self.daily_rsi) 
                and self.weekly_rsi[-1] < self.lower_bound
                and self.daily_rsi[-2] < self.weekly_rsi[-1]):
            self.buy()

bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)

stats = bt.run()

print(stats)

bt.plot()