# -*- coding: utf-8 -*-

'''
作者：IT里的交易员_CSDN
用途：将股票行情dataframe数据写入redis，并进行读取和删除。
注意：本文仅为演示，实操应用代码比较长，恕无法全部展示。
'''

# 使用本文代码，需要提前安装以下两个包，并提前下载Ashare包
# pip install redis
# pip install pickle

import time
# time.sleep(5)# 滞后5秒，等待wsl启动Ubuntu 及 redis。仅做测试，可将此行注释。

import redis
import pickle
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=False)
rs = redis.Redis(connection_pool=pool)

# 下载Ashare.py放到和这个文件相同目录下
from Ashare import get_price

# 计时开始
time11 = time.time()

if 1:
    # 提取行情并写入redis
    df=get_price('sh000001',frequency='1d',count=1000)      #支持'1d'日, '1w'周, '1M'月  
    print('上证指数日线行情\n',df)
    print('r.set 将df写入redis')
    df_bytes = pickle.dumps(df)
    rs.set('df', df_bytes)
    
if 1:  
    # 遍历并redis数据库
    rs_keys=rs.scan_iter()
    for key in rs_keys:
        print('redis现有键',key)

        if 1:
            # 读取键值
            df_bytes_from_redis = rs.get(key)
            if not df_bytes_from_redis is None:
                df = pickle.loads(df_bytes_from_redis)
                print('提取redis现有键值到df',df)
        if 1:
            # 删除键值
            rs.delete(key)
            print('redis现有键',key,'已删除')    
    
# 计时结束    
time21 = time.time()
print("Python操作redis耗时:",time21-time11,'秒')
