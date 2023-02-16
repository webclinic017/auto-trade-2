import time
# import schedule
# import asyncio

import pandas as pd

# import requests
# import aiohttp

import ccxt

exchange = ccxt.okex({
    'enableRateLimit': True,  # 限速设置
    'rateLimit': 1000,       # 限速频率，单位毫秒
    'options': {
        'createMarketBuyOrderRequiresPrice': False
    }
})

symbol = 'BTC/USDT'
timeframe = '1d'
kline = exchange.fetch_ohlcv(symbol, timeframe)
while True:
    try:
        start_time = time.time()
        ticker = exchange.fetch_ticker(symbol)
        ticker = exchange.fetch_ticker(symbol)
        print(f'cost time: {time.time() - start_time}')

        # df = pd.DataFrame.from_dict(ticker)
        # df = pd.read_json(ticker)
        df = pd.json_normalize(ticker)
        print(df)
        time.sleep(0.2)
        print(f'cost time with sleep: {time.time() - start_time}')
    except ccxt.NetworkError as e:
        print(f'cost time: {time.time() - start_time}, error: {e}')
        print(e)
    except ccxt.ExchangeError as e:
        print(f'cost time: {time.time() - start_time}, error: {e}')
        print(e)