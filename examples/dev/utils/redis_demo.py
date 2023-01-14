import redis

"""
pip install redis
"""

# 创建数据库链接
r = redis.Redis(
    host="ip",    # redis的ip
    password="password",   # 密码
    port=6379,    # 端口号，默认6379
    db=0,      # 指定操作redis中的哪个库，redis有16个库0-15
    decode_responses=True  # 返回的结果会自动把bytes类型转为字符串
	)

# string类型数据操作
r.set("aaa","352v235235t",100) # 新增和修改数据，100为失效时间，单位是s，失效时间可不指定
r.delete("aaa") # 删除数据
print(r.get("aaa")) # 查询数据，返回结果为“b'352v235235t'”，返回是bytes类型
print(r.get("aaa").decode()) # 将字节类型转为字符串类型，如果创建数据库链接时，指定decode_responses=True，则不需要在进行类型转换。
print("aaa".encode())  # 把字符串转成bytes

# hash类型数据操作
r.hset("stu","lili1",'{"id":1,"username":"xxx"}')  # 新增和修改数据
print(r.hdel("stu","lili1"))  # 删除数据
print(r.hget("stu","lili1"))  # 查询数据
print(r.hgetall("stu"))   # 查询全部数据
# 将redis返回的bytes类型转换为字典
d={}
for k,v in r.hgetall("stu").items():
    k = k.decode()
    v = v.decode()
    d[k] = v
print(d)

r.flushdb()   # 只清空当前数据库的数据
r.flushall()  # 清空所有数据库里面的所有数据
r.expire("stu",100) # 对key设置过期时间
print(r.keys())   # 获取当前数据库里面所有的key
print(r.keys("*stu*")) # 模糊匹配，查找数据库中含有“stu”的key
print(r.exists("aaa"))  # 查看某个key是否存在，0代表不存在，1代表存在
print(r.type("aaa")) # 查看key的类型
