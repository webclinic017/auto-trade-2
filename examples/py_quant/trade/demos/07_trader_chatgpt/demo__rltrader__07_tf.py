import numpy as np
import random
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense

"""
tensorflow Hedge Strategy

不包含环境 environment （如 backtrader，gym 等）
"""

class HedgeStrategy:
    def __init__(self, state_size, action_size, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.dqn = self.build_model()
        
    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=keras.optimizers.legacy.Adam(lr=0.001))
        return model
    
    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.dqn.predict(state)
        return np.argmax(act_values[0])
    
    def update_dqn(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + 0.95 * np.amax(self.dqn.predict(next_state)[0])
        target_f = self.dqn.predict(state)
        target_f[0][action] = target
        self.dqn.fit(state, target_f, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


