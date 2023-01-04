import gym

# stable_baselines
# from stable_baselines.common.policies import MlpPolicy
# from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import PPO2

# stable_baselines3
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3 import PPO

from envs.StockTradingEnv import StockTradingEnv

import pandas as pd

df = pd.read_csv('./data/MSFT.csv')
df = df.sort_values('Date')

# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: StockTradingEnv(df)])

# stable_baselines
# model = PPO2(MlpPolicy, env, verbose=1)

# stable_baselines3
model = PPO("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=50)

obs = env.reset()
for i in range(len(df['Date'])):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render(title="MSFT")
