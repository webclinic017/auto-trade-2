from jqdata import *

# 创证纳金 20 20

g.signal = 'KEEP'
g.lag1 = 13  #比价周期
g.lag2 = 13  #均线周期
g.last = '0' #保存持仓股票代码
g.ETFList = np.array([
    ['518880.XSHG','518880.XSHG'], #黄金ETF  518880
    # ['513100.XSHG','513100.XSHG'], #纳指ETF  513100
    ['399006.XSHE','159915.XSHE'], #创业板 399006 159915 159952 512900
    # ['513050.XSHG','513050.XSHG'], #中概互联 ETF  
    # ['399673.XSHE','399673.XSHE'], #创业板50 399673 159949
    ['000016.XSHG','000016.XSHG'], #上证50 000016 510050 510710 510850
    # ['000300.XSHG','510300.XSHG'], #沪深300
    ['000905.XSHG','510500.XSHG'] #中证500
    # ['399975.XSHE','399975.XSHE'], #证劵公司 399975 512880 512000 512900
    # ['399987.XSHE','399987.XSHE'], #中证酒
    # ['515650.XSHG','515650.XSHG'], #消费50
    # ['000913.XSHG','000913.XSHG'], #300医药 000913 399913 000913
    # ['512760.XSHG','512760.XSHG'], #中华半导体
    # ['399932.XSHE','159928.XSHE'], #消费ETF
    # ['515000.XSHG','515000.XSHG'], #科技 515000
    # ['000015.XSHG','510880.XSHG'], #红利ETF
    # ['512290.XSHG','512290.XSHG'], #生物医药ETF
    # ['512170.XSHG','512170.XSHG'], #医疗ETF
    # ['512010.XSHG','512010.XSHG'], #医药ETF
    # ['512690.XSHG','512690.XSHG'], #酒ETF
    # ['159928.XSHE','159928.XSHE'], #消费ETF
    # ['512760.XSHG','512760.XSHG'], #芯片ETF
    # ['512480.XSHG','512480.XSHG'], #半导体ETF
])

'''
=================================================
总体回测前设置参数和回测
=================================================
'''
def initialize(context):
    set_params()    #设置参数
    set_backtest()  #设置回测条件
    run_daily(ETFtrade1, time='14:50') #信号确认
    run_daily(ETFtrade2, time='14:52') #下单交易

# 设置参数
def set_params():
    # 设置基准收益
    set_benchmark('000300.XSHG')

# 设置回测条件
def set_backtest():
    set_option('use_real_price', True) #用真实价格交易
    log.set_level('order', 'error')

#每天开盘前要做的事情
def before_trading_start(context):
    set_slip_fee(context) 

# 根据不同的时间段设置滑点与手续费
def set_slip_fee(context):
    # 将滑点设置为0
    set_slippage(FixedSlippage(0)) 
    # 根据不同的时间段设置手续费
    set_commission(PerTrade(buy_cost=0.0005, sell_cost=0.0005, min_cost=5)) 

'''
=================================================
每日信号确认及交易
=================================================
''' 
def ETFtrade1(context): #信号确认函数
    g.signal = get_signal(context)
    
def ETFtrade2(context): #交易函数
    if g.signal == 'sell_the_stocks': #卖出持仓股票
        sell_the_stocks(context)
    elif g.signal == 'KEEP': #保持持仓不变
        return
    else:
        sell_the_stocks(context) #卖出持仓股票
        buy_the_stocks(context,g.signal) #买入股票

#获取交易信号
def get_signal(context):
    i=0 # 计数器初始化
    df = pd.DataFrame()
    for row in g.ETFList:
        security = row[0]
    # 获取指数的历史收盘价
        close_data = attribute_history(security, g.lag1, '1d', ['close'],df=False)
    # 获取指数当前收盘价
        current_data = get_current_data()
        current_price = current_data[security].last_price
    # 获取指数票的阶段收盘价涨幅百分比
        cp_increase = 100*(current_price/close_data['close'][0]-1)
    # 获取指数的收盘价
        close_data = attribute_history(security, g.lag2, '1d', ['close'],df=False)
    # 取得过去 g.lag2 天的平均价格
        ma_n1 = (current_price+close_data['close'].sum()-close_data['close'][0])/g.lag2
    # 计算最新收盘价与均线差值    
        pre_price = current_price - ma_n1
        df.loc[i,'代码'] = row[1] # 把标的股票代码添加到DataFrame
        df.loc[i,'涨幅'] = cp_increase # 把计算结果添加到DataFrame
        df.loc[i,'均线差'] = pre_price # 把计算结果添加到DataFrame
        i=i+1
    # 对计算结果表格进行排序
    df.sort_values(by='涨幅',ascending=False,inplace=True) # 按照涨幅排序
    df.reset_index(drop=True, inplace=True)
    log.info("行情表格:\n %s" % (df)) # 输出计算结果
    
    if df.iloc[0,1] > 0 and df.iloc[0,2] > 0: #判断持有条件：涨幅为正，站上13日均线
        signal = True #排名第一的股票符合持有条件
    else:
        signal = False  #排名第一的股票不符合持有条件
    
    if g.last == '0' and signal == True:# 持仓为空，第一名符合持有条件
        g.last = df.iloc[0,0]
        log.info("交易信号:买入 %s" % (df.iloc[0,0]))
        return df.iloc[0,0]
    
    if g.last == '0' and signal == False:# 持仓为空，第一名不符合持有条件
        log.info("交易信号:保持空仓")
        return 'KEEP'# 持仓不变

    if g.last != df.iloc[0,0] and signal == True: # 持仓未排第一，第一名符合持有条件
        g.last = df.iloc[0,0]
        log.info("交易信号:买入 %s" % (g.last))
        return df.iloc[0,0]

    if g.last != df.iloc[0,0] and signal == False: # 持仓未排第一，第一名不符合持有条件
        log.info("交易信号:卖出 %s" % (g.last))
        g.last = '0'
        return 'sell_the_stocks'
    
    if g.last == df.iloc[0,0] and signal == True: # 持仓股排名第一，符合持有条件
        log.info("交易信号:继续持有 %s" % (g.last))
        return  'KEEP'    
    
    if g.last == df.iloc[0,0] and signal == False: # 持仓股排名第一，不符合持有条件
        log.info("交易信号:卖出 %s" % (g.last))
        g.last = '0'
        return 'sell_the_stocks'
 
#卖出股票
def sell_the_stocks(context):
    for stock in context.portfolio.positions.keys():
        return (log.info("正在卖出 %s" % stock), order_target_value(stock, 0))

#买入股票
def buy_the_stocks(context,signal):
    return (log.info("正在买入 %s"% signal ),order_value(signal,context.portfolio.cash))