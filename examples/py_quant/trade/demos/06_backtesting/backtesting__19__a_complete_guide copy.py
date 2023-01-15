import datetime
import pandas_ta as ta
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
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

if True:
    # 运行回测
    stats = bt.run()
else:    
    """
    One really powerful feature of Backtesting.py is the ability 
    to optimize the parameters used in your strategy. 
    
    You can select a range of values for any of the class variables defined in your strategy 
    and it will grid-search to find the best portfolio for whatever metric you've defined.
    
    To get this running for yourself, simply replace stats=bt.run() with:
    """
    # 参数优化
    stats = bt.optimize(
        upper_bound = range(50,85,5),
        lower_bound = range(15,45,5),
        rsi_window = range(10,30,2),
        maximize='Equity Final [$]')

    """
    For maximize you can set any statistic that appears in the stats dataframe, 
    like the Sharpe ratio, the win rate, etc.
    
    Note that the optimizer always assumes higher is better, 
    so if you put volitility as the parameter to optimize it will find the most volitile portfolio.
    
    The stats you get in return will be the stats of the best performing set of parameters.
    You can find the exact parameters used either in the url of the web page that opens up, 
    or else by indexing into stats and accessing the class variables
    """

    """
    >> strategy = stats["_strategy"]
    >> strategy.upper_bound
    75
    >> strategy.lower_bound
    20
    """

# def optim_func(series):
#     """
#     Custom Optimization Functions
#     """
#     if series['# Trades'] < 10:
#         return -1
#     else:
#         return series['Equity Final [$]']/series['Exposure Time [%]']

# stats = bt.optimize(
#         upper_bound = range(50,85,5),
#         lower_bound = range(15,45,5),
#         rsi_window = range(10,30,2),
#         maximize=optim_func)

# stats, heatmap = bt.optimize(
#         upper_bound = range(50,85,5),
#         lower_bound = range(15,45,5),
#         rsi_window = range(10,30,2),
#         maximize='Equity Final [$]',
#         return_heatmap=True)

# # choose your colormaps from here
# # https://matplotlib.org/stable/tutorials/colors/colormaps.html
# hm = heatmap.groupby(["upper_bound","lower_bound"]).mean().unstack()
# sns.heatmap(hm, cmap="plasma")

bt.plot()