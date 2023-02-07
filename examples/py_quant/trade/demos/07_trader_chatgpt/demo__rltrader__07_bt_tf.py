import numpy as np
import pandas as pd
import random
import backtrader as bt
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from collections import deque

from backtesting.test import GOOG

"""
tensorflow Hedge Strategy
"""

class HedgeStrategy(bt.Strategy):
    def __init__(self, state_size=1, action_size=2, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, gamma=0.95):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.gamma = gamma
        self.batch_size = 32
        self.max_treward = 0
        self.averages = list()
        self.memory = deque(maxlen=2000)

        self.dqn = self.build_model()
        self.model = self.dqn
        
        self.order = None
        
    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=0.001))
        return model
    
    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.dqn.predict(state)
        return np.argmax(act_values[0])
    
    def update_dqn(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            # target = reward + 0.95 * np.amax(self.dqn.predict(next_state)[0])
            target = reward
            if next_state:
                target = reward + 0.95 * np.amax(self.dqn.predict(next_state)[0])

        target_f = self.dqn.predict(state)
        target_f[0][action] = target
        self.dqn.fit(state, target_f, epochs=1, verbose=1)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def replay(self):
        batch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in batch:
            if not done:
                if next_state:
                    reward += self.gamma * np.amax(
                        self.model.predict(next_state)[0])
                # else:
                #     reward += 1
            target = self.model.predict(state)
            target[0, action] = reward
            self.model.fit(state, target, epochs=1, verbose=1)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    # def learn(self, episodes):
    #     trewards = []
    #     for e in range(1, episodes + 1):
    #         state = env.reset()
    #         state = np.reshape(state, [1, self.osn])
    #         for _ in range(5000):
    #             action = self.act(state)
    #             next_state, reward, done, info = env.step(action)
    #             next_state = np.reshape(next_state,
    #                                     [1, self.osn])
    #             self.memory.append([state, action, reward,
    #                                  next_state, done])
    #             state = next_state
    #             if done:
    #                 treward = _ + 1
    #                 trewards.append(treward)
    #                 av = sum(trewards[-25:]) / 25
    #                 self.averages.append(av)
    #                 self.max_treward = max(self.max_treward, treward)
    #                 templ = 'episode: {:4d}/{} | treward: {:4d} | '
    #                 templ += 'av: {:6.1f} | max: {:4d}'
    #                 print(templ.format(e, episodes, treward, av,
    #                                    self.max_treward), end='\r')
    #                 break
    #         if av > 195 and self.finish:
    #             break
    #         if len(self.memory) > self.batch_size:
    #             self.replay()
    #     print()

    # def test(self, episodes):
    #     trewards = []
    #     for e in range(1, episodes + 1):
    #         state = env.reset()
    #         for _ in range(5001):
    #             state = np.reshape(state, [1, self.osn])
    #             action = np.argmax(self.model.predict(state)[0])
    #             next_state, reward, done, info = env.step(action)
    #             state = next_state
    #             if done:
    #                 treward = _ + 1
    #                 trewards.append(treward)
    #                 print('episode: {:4d}/{} | treward: {:4d}'
    #                       .format(e, episodes, treward), end='\r')
    #                 break
    #     return trewards
        
    # def next(self):
    #     self.update_dqn(self.datas[0].close)

    def next(self):
        state = self.datas[0].close
        state = np.array([state[0]])
        action = self.choose_action(state)
        
        if action == 0:
            if self.order:
                self.sell()
        elif action == 1:
            if not self.order:
                self.buy()

        if True:
            """replay buffer"""
            reward = 1
            next_state = None
            done = len(self.datas[0].close) >= (self.datas[0].close.buflen() - 1)
            # memory last next_state
            if len(self.memory) > 0:
                self.memory[len(self.memory) - 1][3] = state 

            self.memory.append([state, action, reward, next_state, done])
            if len(self.memory) > self.batch_size:
                self.replay()
        else:
            reward = 1
            next_state = None
            done = len(self.datas[0].close) >= (self.datas[0].close.buflen() - 1)
            self.update_dqn(state, action, reward, next_state, done)

    def notify_order(self, order):
        if order.status in [order.Completed, order.Cancelled, order.Margin]:
            pass
        if not order.alive():
            self.order = None


cerebro = bt.Cerebro()
cerebro.addstrategy(HedgeStrategy)

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

cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(0.0002)
cerebro.run()
cerebro.plot()

