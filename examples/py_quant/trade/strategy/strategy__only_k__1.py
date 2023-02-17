import ccxt
import pandas as pd
import time

import matplotlib.pyplot as plt

"""
chatgpt:

python ccxt okex btc 裸 K 交易策略

裸 K 交易是一种基于 K 线技术分析的交易策略，即利用价格图形和K线指标来判断市场趋势和交易机会，
不依赖于任何其他指标或交易信号。

在 CCXT 库中，我们可以使用 okex 交易所的 API 来实现 BTC 的裸 K 交易策略。

下面是一个基本的示例代码，演示如何使用 CCXT API 从 OKEX 交易所获取 BTC 的 K 线数据，

并对K线数据进行简单的技术分析，根据分析结果做出买卖决策：

在下面的代码中，我们首先使用 ccxt 库中的 okex() 函数创建了一个 OKEX 交易所的 API 对象，
并指定了交易对 BTC/USDT 和 K 线的时间间隔为 1 天。然后，
我们使用 fetch_ohlcv() 方法从 OKEX 交易所获取了 BTC/USDT 的 K 线数据，
并将数据转换为 pandas dataframe 进行后续处理。

在技术分析部分，我们使用 rolling() 函数计算了 K 线的 5 日和 10 日移动平均线，
并根据两条移动平均线的交叉情况判断市场趋势和交易信号。

在裸 K 交易部分，我们根据交易信号做出买卖决策，
即当 5 日移动平均线上穿 10 日移动平均线时，买入BTC；
当5日移动平均线下穿10日移动平均线时，卖出BTC
"""

# 从OKEX交易所获取BTC的K线数据
exchange = ccxt.okex()
symbol = 'BTC/USDT'
timeframe = '1m'
kline = exchange.fetch_ohlcv(symbol, timeframe, limit=1000)

# 将K线数据转换为pandas dataframe
df = pd.DataFrame(kline, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# 对K线数据进行技术分析，判断市场趋势和交易信号
df['ma5'] = df['close'].rolling(window=5).mean()
df['ma10'] = df['close'].rolling(window=10).mean()
df['ma20'] = df['close'].rolling(window=20).mean()
df['signal'] = 0
df.loc[(df['ma5'] > df['ma10']), 'signal'] = 1

# 实现裸K交易策略，根据交易信号做出买卖决策
positions = [""]
for i in range(1, len(df)):
    if df.loc[i-1, 'signal'] == 0 and df.loc[i, 'signal'] == 1:
        positions.append('buy')
    elif df.loc[i-1, 'signal'] == 1 and df.loc[i, 'signal'] == 0:
        positions.append('sell')
    else:
        positions.append('hold')
df['position'] = positions

df_results = df[['timestamp', 'close', 'ma5', 'ma10', 'signal', 'position']]
df_results.to_csv("./btc_ustd__1m__ma5_ma10__results.csv")
# 输出交易信号和买卖决策结果
print(df_results)
df_results.plot()
plt.plot()
