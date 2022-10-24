import time
import redis 
"""
pip install redis
pip install redis-py-cluster
"""

"""
[root@localhost ~]# redis-cli -c -h 192.168.11.15 -p 8001 
192.168.11.15:8001> GET book 
"Python"
"""
# Redis 单机
def redis_mono_test():
    r = redis.Redis(
        host='127.0.0.1', 
        port=6379, 
        db=0, 
        password='123456', 
        decode_responses=True,
        socket_timeout=10,
    ) 
    r.set('password', 'abcdef') 
    print(r.get('password'))
    r.delete("redis.list.1")
    start_time = time.time()
    r.lpush("redis.list.1", 11, 22, 33)
    print(f'cost time lpush: {time.time() - start_time}')
    print(r.lrange('redis.list.1', 0, -1))

## Redis 集群
def redis_cluter_test():
    from rediscluster import RedisCluster 
    # Redis 集群各节点的主机IP地址和端口 
    cluster_nodes = [{'host': '192.168.11.15', 'port': 8001}, 
              {'host': '192.168.11.15', 'port': 8002}, 
              {'host': '192.168.11.15', 'port': 8003}, 
              {'host': '192.168.11.15', 'port': 8004}, 
              {'host': '192.168.11.15', 'port': 8005}, 
              {'host': '192.168.11.15', 'port': 8006}] 
 
    cluster = RedisCluster(startup_nodes=cluster_nodes) 
    cluster.set('book', 'Python') 
    print(cluster.get('password'))

def redis_string_test():
    import redis

    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.set('food', 'mutton', ex=3)    # key是"food" value是"mutton" 将键值对存入redis缓存
    print(r.get('food'))  # mutton 取出键food对应的值

def redis_hash_test():
    import redis
    import time

    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    r.hset("hash1", "k1", "v1")
    r.hset("hash1", "k2", "v2")
    print(r.hkeys("hash1")) # 取hash中所有的key
    print(r.hget("hash1", "k1"))    # 单个取hash的key对应的值
    print(r.hmget("hash1", "k1", "k2")) # 多个取hash的key对应的值
    r.hsetnx("hash1", "k2", "v3") # 只能新建
    print(r.hget("hash1", "k2"))

def redis_list_test():
    import redis
    import time
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.lpush("redis.list.1", 11, 22, 33)
    print(r.lrange('redis.list.1', 0, -1))

def redis_set_test():
    import redis
    import time
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.sadd("set1", 33, 44, 55, 66)  # 往集合中添加元素
    print(r.scard("set1"))  # 集合的长度是4
    print(r.smembers("set1"))   # 获取集合中所有的成员

def redis_orderedset_test():
    import redis
    import time

    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    r.zadd("zset1", n1=11, n2=22)
    r.zadd("zset2", 'm1', 22, 'm2', 44)
    print(r.zcard("zset1")) # 集合长度
    print(r.zcard("zset2")) # 集合长度
    print(r.zrange("zset1", 0, -1))   # 获取有序集合中所有元素
    print(r.zrange("zset2", 0, -1, withscores=True))   # 获取有序集合中所有元素和分数

def redis_orderedset_test():
    import redis
    import time

    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    # pipe = r.pipeline(transaction=False)    # 默认的情况下，管道里执行的命令可以保证执行的原子性，执行pipe = r.pipeline(transaction=False)可以禁用这一特性。
    # pipe = r.pipeline(transaction=True)
    pipe = r.pipeline() # 创建一个管道

    pipe.set('name', 'jack')
    pipe.set('role', 'sb')
    pipe.sadd('faz', 'baz')
    pipe.incr('num')    # 如果num不存在则vaule为1，如果存在，则value自增1
    pipe.execute()

    print(r.get("name"))
    print(r.get("role"))
    print(r.get("num"))

def redis_Bitmap_test():
    pass
def redis_HyperLogLog_test():
    pass

if __name__ == '__main__':
    redis_mono_test()