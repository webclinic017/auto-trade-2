import websocket
import pandas as pd
import json
from datetime import datetime

"""
chatgpt
python 实时缓存 tick 快照数据，并合成一分钟 k线数据
"""

class TickData:
    def __init__(self):
        self.data = pd.DataFrame(columns=["timestamp", "price", "quantity"])

    def add_tick(self, tick):
        self.data = self.data.append(tick, ignore_index=True)

    def generate_k_line(self, interval="1min"):
        self.data.set_index("timestamp", inplace=True)
        k_line_data = self.data.resample(interval).agg({
            "price": "ohlc",
            "quantity": "sum"
        })
        self.data = self.data[self.data.index >= k_line_data.index[-1]]
        return k_line_data

tick_data = TickData()

def on_message(ws, message):
    # 将收到的消息解码为 JSON 字典
    data = json.loads(message)
    tick = {
        "timestamp": datetime.fromtimestamp(data["timestamp"]),
        "price": data["price"],
        "quantity": data["quantity"]
    }

    # 添加新的 "Tick" 数据
    tick_data.add_tick(tick)

    # 生成 1 分钟 K 线数据
    k_line_data = tick_data.generate_k_line()
    # 执行其他操作
    # ...

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("Closed connection")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://data-source-url",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
