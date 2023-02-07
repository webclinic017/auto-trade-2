import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable

"""
pytorch Hedge Strategy

不包含环境 environment （如 backtrader，gym 等）
"""

class DQN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class HedgeStrategy:
    def __init__(self, environment, portfolio, trading_cost):
        self.environment = environment
        self.portfolio = portfolio
        self.trading_cost = trading_cost
        self.dqn = DQN(input_dim=self.environment.observation_space,
                      hidden_dim=16,
                      output_dim=self.environment.action_space)
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.dqn.parameters(), lr=0.01)

    def choose_action(self, state):
        state = torch.Tensor(state)
        state = Variable(state)
        q_values = self.dqn(state)
        action = q_values.max(0)[1].data.numpy()[0]
        return action

    def update_dqn(self, state, action, reward, next_state):
        state = torch.Tensor(state)
        next_state = torch.Tensor(next_state)
        state, next_state = Variable(state), Variable(next_state)
        q_values = self.dqn(state)
        next_q_values = self.dqn(next_state)
        q_value = q_values[action]
        next_q_value = next_q_values.max()
        expected_q_value = reward + 0.99 * next_q_value
        loss = self.criterion(q_value, expected_q_value)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def trade(self, num_steps):
        for step in range(num_steps):
            state = self.environment.get_state()
            action = self.choose_action(state)
            reward, next_state = self.environment.step(action)
            self.update_dqn(state, action, reward, next_state)
            self.portfolio.update(action, reward, self.trading_cost)
