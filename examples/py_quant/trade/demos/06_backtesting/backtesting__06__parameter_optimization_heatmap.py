import datetime
import pandas_ta as ta
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover, plot_heatmaps
from backtesting.test import GOOG

class RsiOscillator(Strategy):

    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    # Do as much initial computation as possible
    def init(self):
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)

    # Step through bars one by one
    # Note that multiple buys are a thing here
    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()

bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)

def optim_func(series):
    """
    Custom Optimization Functions
    """
    if series['# Trades'] < 10:
        return -1
    else:
        return series['Equity Final [$]']/series['Exposure Time [%]']

stats, heatmap = bt.optimize(
        upper_bound = range(55,85,5),
        lower_bound = range(15,45,5),
        rsi_window = range(10,45,5),
        maximize = 'Sharpe Ratio',
        # maximize = optim_func,
        constraint= lambda param:param.upper_bound > param.lower_bound,
        return_heatmap=True)

print(stats)
print(heatmap)

# hm = heatmap.groupby(["upper_bound", "lower_bound"]).mean().unstack()
# sns.heatmap(hm)
# plt.show()

# print(hm)

plot_heatmaps(heatmap, agg="mean")

# bt.plot()