import backtrader as bt
import backtrader.indicators as btind
import numpy as np
import scipy.signal as signal
from scipy import stats
from gym import spaces
from btgym import BTgymEnv, BTgymStrategy, BTgymDataset
from btgym.a3c import Launcher, LSTMPolicy

class MyStrategy(BTgymStrategy):
    def __init__(self, **kwargs):
        super(MyStrategy,self).__init__(**kwargs)
        self.order_penalty = 1
        self.trade_just_closed = False
        self.trade_result = None
    
    def notify_trade(self, trade):    
        if trade.isclosed:
            # Set trade flag and result:
            self.trade_just_closed = True
            self.trade_result = trade.pnlcomm

    def get_state(self):
        T = 1e3 
        # amplifier
        X = np.gradient(self.raw_state, axis=0)
        X *= T
        self.state['model_input'] = X 
        return self.state

    def get_reward(self):
        r = (self.broker.get_value() / self.env.broker.startingcash -1) * 10

        if self.trade_just_closed:
            r += self.trade_result
            self.trade_just_closed = False

        if self.order_failed:
            r -= self.order_penalty
            self.order_failed = False
        
        return r / 20  
    
time_embed_dim = 30

state_shape = {
    'raw_state': spaces.Box(low=-1, high=1, shape=(time_embed_dim, 4)),
    'model_input': spaces.Box(low=-100, high=100, shape=(time_embed_dim, 4))
}

MyCerebro = bt.Cerebro()
MyCerebro.addstrategy(
    MyStrategy,
    state_shape=state_shape,
    portfolio_actions=('hold', 'buy', 'sell','close'),
    drawdown_call=5, # max to loose, in percent of initial 
    cashtarget_call=20,  # max to win, 
    sameskip_frame=10,
)

# Set leveraged account:
MyCerebro.broker.setcash(100000)
MyCerebro.broker.setcommission(commission=0.0001, leverage=1) 
# commisssion to imitate spread
MyCerebro.broker.set_shortcash(False)
MyCerebro.addsizer(bt.sizers.SizerFix, stake=10000,)

MyCerebro.addanalyzer(bt.analyzers.DrawDown)

MyDataset = BTgymDataset(
    filename='../data/test_sine_wave.csv',
    start_weekdays=[0, 1, 2, 3, ],
    episode_len_days=1,
    episode_len_hours=23,
    episode_len_minutes=0,
    start_00=False,
    time_gap_hours=2,
)

env_config = dict(
    dataset=MyDataset,
    engine=MyCerebro,
    render_modes=['episode', 'human', 'model_input'],
    render_state_as_image=True,
    render_ylabel='OHLC Price Gradients',
    render_size_episode=(12,8),
    render_size_human=(8, 3.5),
    render_size_state=(10, 5),
    render_dpi=75,
    port=5100,
    data_port=5099,
    connect_timeout=60,
    verbose=0,
)

# Set tensorflow distributed cluster and a3c configuration:
cluster_config = dict(host='127.0.0.1',port=42222,num_workers=8,num_ps=1,)
launcher = Launcher(
    cluster_config=cluster_config,
    env_class=BTgymEnv,
    env_config=env_config,
    policy_class=LSTMPolicy,
    rollout_length=20,
    test_mode=False,
    train_steps=1000000000,
    model_summary_freq=20,
    episode_summary_freq=1,
    env_render_freq=10,
    verbose=1
)