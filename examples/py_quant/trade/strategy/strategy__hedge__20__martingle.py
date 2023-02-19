import ccxt
import time

"""
实现一个数字货币马丁格尔实盘策略

马丁格尔策略是一种逐步加仓的交易策略，可以用于数字货币等交易市场。
下面是一个简单的实现数字货币马丁格尔实盘策略的 Python 示例代码：
"""

# 定义交易对和交易所
symbol = 'ETH/USDT'
exchange = ccxt.okex({
    'apiKey': '7ae95e84-753d-432d-87e2-5d627b9b81a2',
    'secret': 'FCB5572D427DECDE2A0855ED509FF823',
    'password': 'Dbok5&18',
    'enableRateLimit': True
})

# 定义初始订单量和初始订单价格
order_size = 0.001
init_price = exchange.fetch_ticker(symbol)['last']

# 定义马丁格尔参数
martingale_factor = 2
stop_loss_factor = 0.95
max_buy_levels = 5

# 定义交易函数
def buy_next_level(current_price, level, size):
    new_price = current_price * martingale_factor
    new_order = exchange.create_order(symbol, 'limit', 'buy', size, new_price)
    print(f'Bought {size} {symbol} at {new_price} (level {level})')
    return new_price, size

def sell_all(position, price, level):
    sell_order = exchange.create_order(symbol, 'limit', 'sell', position, price)
    print(f'Sold {position} {symbol} at {price} (level {level})')

# 定义主程序
current_level = 1
current_price = init_price

while True:
    # 获取当前价格和账户信息
    current_price = exchange.fetch_ticker(symbol)['last']
    balance = exchange.fetch_balance()['USDT']['free']

    print(f"current_price: {current_price}")
    print(f"balance: {balance}")
    print(f"current_level: {current_level}")
    if True:
        break;
    
    # 检查是否需要停止交易
    if current_price < init_price * stop_loss_factor:
        print('Stop loss reached. Exiting.')
        break
        
    # 如果达到最大买入级别，则等待
    if current_level > max_buy_levels:
        time.sleep(60)
        continue
        
    # 判断是否需要买入
    if balance > order_size:
        buy_next_level(current_price, current_level, order_size)
        current_level += 1
        
    # 判断是否需要卖出
    positions = exchange.fetch_positions(symbol)
    if positions:
        current_position = positions[0]['amount']
        if current_position > 0:
            sell_all(current_position, current_price, current_level)
            current_level = 1
            
    # 等待60秒后再执行下一次交易
    time.sleep(60)
