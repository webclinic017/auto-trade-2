import ccxt
"""
您可以使用 CCXT 库来连接 OKEx API，然后使用 Python 编写对冲套利策略。
对冲套利需要两个交易所的账户，这里我们假设您已经有 OKEx 的账户并已完成 KYC 验证，有足够的资金买卖 BTC。

以下是一个简单的 BTC 对冲套利策略的代码示例：
"""

# 初始化交易所
exchange1 = ccxt.okex({
    # 'apiKey': 'YOUR_API_KEY',
    # 'secret': 'YOUR_SECRET_KEY',
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True,
})
exchange2 = ccxt.okex({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True,
})

# 从两个交易所获取 BTC 的最新价格
ticker1 = exchange1.fetch_ticker('BTC/USDT')
ticker2 = exchange2.fetch_ticker('BTC/USDT')

# 计算 BTC 在两个交易所的价差
spread = ticker1['last'] - ticker2['last']

# 如果价差超过一定的阈值，进行对冲套利
if spread > 10:
    # 在第一个交易所卖出 BTC
    order1 = exchange1.create_order('BTC/USDT', 'limit', 'sell', 0.01, ticker1['bid'])
    # 在第二个交易所买入 BTC
    order2 = exchange2.create_order('BTC/USDT', 'limit', 'buy', 0.01, ticker2['ask'])
    print('对冲套利成功')
else:
    print('无法进行对冲套利')

"""
这是一个非常简单的例子，真正的对冲套利策略需要考虑更多因素，
例如交易手续费、市场深度、风险控制等等。在实际交易中，您需要谨慎对待风险并始终注意市场波动。
"""

