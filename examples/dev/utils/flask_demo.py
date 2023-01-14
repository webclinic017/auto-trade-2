import flask   # 微型的Python开发的Web框架
import json

server = flask.Flask(__name__)

# post请求，写死接口返回数据
@server.route('/api/user',methods=['post'])  # 前面是接口路径,methods是请求方式,只有get可以不写，可同时使用post请求和get请求
def user_info():
    d = {"id":1,"username":"lili","age":18}
    return json.dumps(d)
# get请求   
@server.route('/get')
def user2():
    name = flask.request.values.get("name")
    data = {"name":name}
    return json.dumps(data,ensure_ascii=False)

# 获取cookie，获取header
@server.route('/header',methods=['post','get'])  
def user3():
    name = flask.request.headers.get("hhhh")  # 从header里获取数据
    time = flask.request.cookies.get("time")   # cookie获取数据
    data = {"hhhh":name,"time":time}
    return json.dumps(data)

# 入参是json格式
@server.route('/json',methods=['post'])  
def user4():
    if flask.request.is_json:
        age = flask.request.json.get("age")
        name = flask.request.json.get("name")
        sex = flask.request.json.get("sex")
        data = {"age": age, "name": name, "sex": sex}
    else:
        data = {"code": -1, "message": "入参不是json"}
    return json.dumps(data, ensure_ascii=False)

# 上传文件
@server.route('/file',methods=['post'])
def user5():
    file = flask.request.files.get("file")
    file.save(file.filename)
    return json.dumps({"code": 0, "msg": "上传成功"}, ensure_ascii=False)

server.run(port=8888,debug=True,host='0.0.0.0')  # host='0.0.0.0'指定这个，在同一个局域网内的均可访问此接口
