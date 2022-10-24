import redis 
"""
pip install redis
pip install redis-py-cluster
"""

# Redis 单机
r = redis.Redis(host='localhost', port=6379, db=0) 
r.set('password', 'abcdef') 
 
print(r.get('password'))

## Redis 集群
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

"""
[root@localhost ~]# redis-cli -c -h 192.168.11.15 -p 8001 
192.168.11.15:8001> GET book 
"Python"
"""