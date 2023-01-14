import hashlib

s ="1234"
bs = s.encode()
m = hashlib.md5(bs)
# m = hashlib.sha256(bs)   #其他加密方式
# m = hashlib.sha512(bs)
# m = hashlib.sha224(bs)
print(m.hexdigest())   # 同样的字符串，使用md5加密后结果都一样。加密后不可逆

# 加盐
s ="1234" + "dfsdffadf#@^$*#"   # 在字符串后面加上随机生成的字符串，这一部分叫盐值

def my_md5(s, salt=""):
    new_s = str(s) + salt
    m = hashlib.md5(new_s.encode())
    return m.hexdigest()
result = my_md5(12345, "ds@#^@")
print(result)

"""
运行结果：
81dc9bdb52d04dc20036dbd8313ed055
762463a6bb94560ad1707d692907a45d
"""

# base64加解密
import base64

# 加密
s = "jejigjfgiwtuiruerweiowq"
result = base64.b64encode(s.encode()).decode()
print(result)

# 解密
s1 = "amVqaWdqZmdpd3R1aXJ1ZXJ3ZWlvd3E="
result = base64.b64decode(s1).decode()
print(result)


