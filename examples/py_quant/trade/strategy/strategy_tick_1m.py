import time
# import schedule
# import asyncio

import pandas as pd

# import requests
# import aiohttp

import ccxt


exchange = ccxt.okex({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True,
})

symbol = 'BTC/USDT'
timeframe = '1m'
period = 20

def sma(data, period=20):
    return sum(data[-period:]) / period

while True:
    try:
        # 获取最新的K线数据
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe)[-period:]
        close_prices = [ohlcv[i][4] for i in range(len(ohlcv))]

        # 计算SMA20指标
        sma20 = sma(close_prices)

        # 获取当前持仓情况和余额
        balance = exchange.fetch_balance()
        position = exchange.fetch_position(symbol)

        # 根据SMA20指标和持仓情况执行交易
        if close_prices[-1] > sma20 and position['notional'] < balance['USDT']:
            # 如果价格在SMA20上方且当前没有持仓，则买入
            exchange.create_market_buy_order(symbol, position['size'])

        if close_prices[-1] < sma20 and position['notional'] > 0:
            # 如果价格在SMA20下方且当前持有仓位，则卖出
            exchange.create_market_sell_order(symbol, position['size'])

    except ccxt.NetworkError as e:
        print('网络错误：', type(e).__name__, str(e))
        continue

    except ccxt.ExchangeError as e:
        print('交易所错误：', type(e).__name__, str(e))
        continue

    except Exception as e:
        print('未知错误：', type(e).__name__, str(e))
        continue

    # 休眠一段时间，避免频繁地查询交易所API
    time.sleep(10)
