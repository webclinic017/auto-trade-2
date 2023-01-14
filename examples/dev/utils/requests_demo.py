import requests

# get请求
url = "http://127.0.0.1:8888/get"
data = {"name": "哈哈哈"}
req = requests.get(url=url, params=data)

print(req.json())  # 把返回的数据转成字典
print(req.text)   # 返回的是字符串
print(req.content) # 返回的是bytes类型
print(req.cookies) # 返回的cookies
print(req.status_code)  # 返回http状态码
print(req.headers)  # 返回响应头

# post请求
url = "http://127.0.0.1:8888/get"
data = {"name": "哈哈哈"}
req = requests.post(url=url, data=data, params={"version": "1.0"})
# params=xx,参数是传在url后面的；data=xxx，参数传在body里面的form-data的
print(req.text)   

# 传header，传cookie
url = "http://127.0.0.1:8888/header"
req = requests.post(url=url, headers={"hhhh": "121112333"}, cookies={"time": "328942837"})   # 把抓包中的cookie中的数据，每个字段都一一做映射
# req = requests.post(url,headers={"hhhh": "121112333", "cookie": "time=sdsds;time2=dfsd"})  # 直接把抓包中的一堆cookie数据放入字典中cookie的value中
print(req.text)

# 入参为json
url = "http://127.0.0.1:8888/json"
data = {"age": 36, "name": "lili", "sex": "女"}
req = requests.post(url, json=data)
print(req.text)

# 上传文件，入参是文件
url = "http://127.0.0.1:8888/file"
files = {"file": open("C:/Users/admin/Desktop/uid.txt", "rb")}
req = requests.post(url, files=files)
print(req.text)

# 下载文件
url = "https://bkimg.cdn.bcebos.com/pic/f9198618367adab4a0cd379e80d4b31c8601e4ca?x-bce-process=image/resize,m_lfit,h_120,limit_1"
req = requests.get(url, verify=False, timeout=5) # 如果遇到https请求报错，加上verify=False；timeout设置网络超时时间

with open("a.jpg", 'wb')as fw:
    fw.write(req.content)
