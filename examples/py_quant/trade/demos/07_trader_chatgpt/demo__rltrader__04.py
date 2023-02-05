import backtrader as bt
import numpy as np
import tensorflow as tf

"""
用 python 以及 backtrader 和 深度强化学习写一个策略代码

这是一个使用 Backtrader 和深度强化学习（Deep Reinforcement Learning）编写交易策略的示例代码：
"""

class DeepRLStrategy(bt.Strategy):
    params = (
        ("window_length", 10),
        ("model_file", "model.h5"),
    )

    def __init__(self):
        self.model = self._load_model()
        self.window_length = self.params.window_length
        self.data_window = np.zeros((1, self.window_length, 4))

    def next(self):
        self.data_window[0,:-1,:] = self.data_window[0,1:,:]
        self.data_window[0,-1,:] = [self.data.open[0], self.data.high[0], self.data.low[0], self.data.close[0]]
        
        action = self.model.predict(self.data_window)[0]
        
        if action == 1:
            self.buy()
        elif action == 2:
            self.sell()
        
    def _load_model(self):
        model = tf.keras.models.load_model(self.params.model_file)
        model.compile(loss="mse", optimizer="adam")
        return model
