import pandas as pd
import numpy as np

class Slope(np.Rolling):
    """
    动量定义为 20日收盘价的“斜率”——就是线性回归的斜率。
    qlib原本的表达式，使用了cpython，这里我们使用np.polyfit即可实现。
    """
    def __init__(self, feature, N):
        super(Slope, self).__init__(feature, N, "slope")

    def _load_internal(self, instrument):
        def calc_slope(x):
            x = x / x[0]  # 这里做了一个“归一化”
            slope = np.polyfit(range(len(x)), x, 1)[0]
            return slope

        series = self.feature.load(instrument)
        result = series.rolling(self.N, min_periods=2).apply(calc_slope)
        series = pd.Series(result, index=series.index)
        return series
 
fields += ['Slope($close,20)']
names += ['mom_slope']

fields += ["Ref($close,-1)/$close - 1"]
names += ['label']

all = Dataloader().load_one_df(['000300.SH'], names, fields)

class SelectTopK:
    def __init__(self, K=1, order_by='order_by', b_ascending=False):
        self.K = K
        self.order_by = order_by
        self.b_ascending = b_ascending

    def __call__(self, context):
        stra = context['strategy']
        features = context['features']

        if self.order_by not in features.columns:
            logger.error('排序字段{}未计算'.format(self.order_by))
            return

        bar = get_current_bar(context)
        if bar is None:
            logger.error('取不到bar')
            return True
        bar.sort_values(self.order_by, ascending=self.b_ascending, inplace=True)

        selected = []
        pre_selected = None
        if 'selected' in context:
            pre_selected = context['selected']
            del context['selected']

        for code in list(bar.code):
            if pre_selected:
                if code in pre_selected:
                    selected.append(code)
            else:
                selected.append(code)
            if len(selected) >= self.K:
                break
        context['selected'] = selected

class PickTime:
    """
    大盘使用沪深300的RSRS给大盘择时。
    """
    def __init__(self, benchmark='000300.SH', signal='signal'):
        self.benchmark = benchmark
        #self.buy = self.buy
        self.signal = signal

    def __call__(self, context):
        stra = context['strategy']
        extra = context['extra']
        df = extra[self.benchmark]

        if self.signal not in df.columns:
            logger.error('择时信号不存在')
            return True

        curr_date = stra.get_current_dt()
        if curr_date not in df.index:
            logger.error('日期不存在{}'.format(curr_date))
            return None

        bar = df.loc[curr_date]
        if type(bar) is pd.Series:
            bar = bar.to_frame().T

        if bar[self.signal][0]:
            logger.info('择时信号显示，平仓所有。')
            context['selected'] = []

'''
光大 RSRS 指标
Backtrader 实现
'''
import backtrader as bt
import numpy as np
import statsmodels.api as sm

class RSRS(bt.Indicator):

    lines = ('rsrs', 'rsrs_dev')

    params = (('N', 18), ('value', 5))

    def __init__(self):
        self.high = self.data.high
        self.low = self.data.low

        self.lines.rsrs = bt.Max(0.0, self.params.value)
        self.lines.rsrs_dev = bt.Min(0.0, self.params.value)

    def next(self):
        high_N = self.high.get(ago=0, size=self.p.N)
        low_N = self.low.get(ago=0, size=self.p.N)

        print(low_N, len(low_N))
        try:
            X = sm.add_constant(np.array(low_N))
            model = sm.OLS(np.array(high_N), X)
            results = model.fit()
            self.lines.rsrs[0] = results.params[1]
        except:
            self.lines.rsrs[0] = 0