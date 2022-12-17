import redis
from rq import Worker, Queue, Connection

listen = ['default']
redis_url = "redis://localhost:6379"  # redis server 默认地址
conn = redis.from_url(redis_url)

def square_function(x):
    return x*x

if __name__ == '__main__':
    with Connection(conn):  # 建立与redis server的连接
        worker = Worker(list(map(Queue, listen)))  # 建立worker监听给定的队列
        worker.work()