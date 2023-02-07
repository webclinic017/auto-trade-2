import backtrader as bt
import numpy as np
import pandas as pd
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from datetime import datetime

from backtesting.test import GOOG

"""
chatgpt
用 python 以及 backtrader 和 深度强化学习写一个策略代码

在 Backtrader 中使用深度强化学习（DQN）编写交易策略需要结合一些外部库，

如 TensorFlow 或 Keras。以下是一个示例，实现了在 Backtrader 中使用 DQN 进行交易的代码：

请注意，这仅是一个示例代码，并不能保证在实际交易中一定能够获利。

在使用 DQN 进行交易时，需要对策略进行充分的测试和优化，以确保它具有足够的稳定性和有效性。

此外，该代码也需要对数据和指标进行处理以计算状态，并且还需要对模型训练进行更详细的设置。

因此，如果您没有相关经验，建议您先了解 DQN 和 Backtrader 的基础知识，再尝试编写代码。
"""

class DeepQAgent(bt.Strategy):
    params = (
        ("batch_size", 32),
        ("gamma", 0.95),
        ("epsilon", 1.0),
        ("epsilon_min", 0.01),
        ("epsilon_decay", 0.995),
        ("learning_rate", 0.001),
    )

    def __init__(self):
        self.state = None
        self.reward = 0
        self.done = False
        self.model = self.build_model()

        # bt.talib.SMA(self.data.close, timeperiod=5)
        sma5 = bt.indicators.SMA(self.data, period=5)
        sma42 = bt.indicators.SMA(self.data, period=42)
        sma170 = bt.indicators.SMA(self.data, period=170)

        # 计算布林带
        # bt.talib.BBANDS(self.data, timeperiod=25)
        # bt.indicators.BollingerBands(self.data, period=25)

    def build_model(self):
        model = Sequential()
        # model.add(Dense(24, input_dim=self.indicators.shape[1], activation="relu"))
        model.add(Dense(24, input_dim=1, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(2, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=self.params.learning_rate))
        return model

    def next(self):
        if self.done:
            # self.state = self.indicators[-1]
            self.state = self.data.close[-1]
            self.done = False

        if np.random.rand() <= self.params.epsilon:
            action = np.random.choice([0, 1])
        else:
            action = np.argmax(self.model.predict(self.state))

        if action == 1:
            if self.data_close[0] > self.data_close[-1]:
                self.reward = 1
            else:
                self.reward = -1
        else:
            self.reward = 0

        self.done = True

    def stop(self):
        if self.params.epsilon > self.params.epsilon_min:
            self.params.epsilon *= self.params.epsilon_decay

cerebro = bt.Cerebro()
cerebro.addstrategy(DeepQAgent)

# data = bt.feeds.YahooFinanceData(dataname="AAPL", fromdate=datetime(2015,1,1), todate=datetime(2020,1,1))
data = GOOG
data.reset_index(inplace=True, drop=False)
print(data)
data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume'];
data['datetime'] = pd.to_datetime(data['datetime'].values)
data.index = pd.to_datetime(data.index.values)
data = data.set_index('datetime')
# data.reset_index(inplace=True, drop=False)
print(data.columns)
print(data)


data = bt.feeds.PandasData(dataname = GOOG)
cerebro.adddata(data, name="GOOG")

cerebro.run()
cerebro.plot()
