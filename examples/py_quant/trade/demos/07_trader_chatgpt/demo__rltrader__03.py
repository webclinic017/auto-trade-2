import backtrader as bt
import numpy as np
from collections import deque
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

"""
https://chat.openai.com/
用 python 以及 backtrader 和 深度强化学习写一个策略代码

如果您想利用 Backtrader 和深度强化学习来写一个交易策略，您可以参考以下步骤：

  1. 安装 Backtrader 和相关的库，如 Numpy 和 Keras。

  2. 定义一个策略类，继承自 Backtrader 的 bt.Strategy 类。

  3. 在策略类的 __init__ 方法中，定义一个神经网络模型，
  使用 Keras 的 Sequential 模型，并加入输入层、隐藏层、输出层。

  4. 定义策略类的 next 方法，该方法是 Backtrader 用来运行策略的主要入口，
  每当有新的数据可用时，Backtrader 都会调用该方法。
  在该方法中，我们可以使用神经网络对当前的状态进行预测，决定是否进行买卖操作。

最后，使用 Backtrader 创建一个回测实例，加载数据，
并将我们刚刚定义的策略类添加到回测实例中，然后运行回测即可。

如果您需要更详细的代码实现，可以参考相关的教程和文档。希望对您有所帮助！
"""

class DeepQLearningStrategy(bt.Strategy):
    params = (
        ('dqn_input_size', 20),
        ('dqn_hidden_size', 128),
        ('dqn_output_size', 3),
        ('memory_capacity', 10000),
        ('batch_size', 64),
        ('epsilon', 0.99),
        ('discount_factor', 0.95),
        ('learning_rate', 0.001)
    )

    def __init__(self):
        self.dqn = Sequential()
        self.dqn.add(Dense(self.params.dqn_hidden_size, input_dim=self.params.dqn_input_size, activation='relu'))
        self.dqn.add(Dense(self.params.dqn_output_size, activation='linear'))
        self.dqn.compile(loss='mse', optimizer=Adam(lr=self.params.learning_rate))
        
        self.memory = deque(maxlen=self.params.memory_capacity)
        self.state = None
        self.action = None
        self.reward = None
        self.next_state = None
        self.done = None
        self.data_len = None
        self.position = None

    def next(self):
        if not self.data_len:
            self.data_len = len(self)

        if self.state is None:
            self.state = np.array([0 for i in range(self.params.dqn_input_size)])
        else:
            self.state = self.next_state

        action = self.dqn.predict(np.array(self.state).reshape(1, -1))
        action = np.argmax(action)

        if self.data.close[0] > self.data.close[-20]:
            action = 0
        elif self.data.close[0] < self.data.close[-20]:
            action = 2
        else:
            action = 1
        
        if self.position:
            if action == 0:
                self.sell()
            elif action == 2:
                self.buy()
        else:
            if action == 2:
                self.buy()

        self.next_state = np.array([(self.data.close[i] - self.data.close[i - 20]) / self.data.close[i - 20] for i in range(-19, 1)])
        self.reward = self.data.close[0] - self.data.close[-1]
        self.memory.append((self.state, action, self.reward, self.next_state, self.done))

        if len(self.memory)
