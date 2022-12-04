import gym 
import sys

"""
pip3 install box2d-py
pip3 install gym[Box_2D]
"""

env = gym.make(sys.argv[1])
env.reset()
for i in range(1000):
    env.render()
    ob, reward, done, info = env.step(env.action_space.sample())
    if done:
        env.reset()