import time
import akshare as ak
import pandas as pd

def generate_k_line(df, interval='1min'):
    df.set_index("timestamp", inplace=True)
    k_line_data = df.resample(interval).agg({
        "price": "ohlc",
        "quantity": "sum"
    })
    df = df[df.index >= k_line_data.index[-1]]
    return k_line_data

def handle_realtime_data(data):
    df = pd.DataFrame(data, columns=["timestamp", "price", "quantity"])
    k_line_data = generate_k_line(df)
    print(k_line_data)

def subscribe_realtime_tick_data(symbol, handle_realtime_data):
    while True:
        time.sleep(1)

if __name__ == "__main__":
    subscribe_realtime_tick_data("sh000001", handle_realtime_data)