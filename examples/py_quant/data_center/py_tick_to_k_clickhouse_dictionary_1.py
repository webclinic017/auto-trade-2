from collections import defaultdict
import datetime

# 记录数据
data_dict = defaultdict(list)

# 收到新的 tick 数据
def process_tick(tick_data):
    # 将 tick 数据添加到数据字典中
    data_dict[tick_data["timestamp"]].append(tick_data)

# 定时调用的函数，用于合并 k 线数据
def merge_k_line_data(k_line_interval):
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 删除过时的数据
    data_dict.pop(current_time - datetime.timedelta(minutes=k_line_interval), None)
    # 遍历剩余数据，统计 k 线数据
    k_line_data = {"open": 0, "close": 0, "high": 0, "low": 0, "volume": 0}
    for tick_data in data_dict.values():
        for d in tick_data:
            k_line_data["open"] = d["open"]
            k_line_data["close"] = d["close"]
            k_line_data["high"] = max(k_line_data["high"], d["high"])
            k_line_data["low"] = min(k_line_data["low"], d["low"])
            k_line_data["volume"] += d["volume"]
    # 将合成的 k 线数据保存到数据库中
    save_to_database(k_line_data)

def save_to_database(data):
    pass