import jsonpath

"""
pip install jsonpath
"""

jsona ={
    "money":19000,
    "hose":{
        "beijing":["三环","四环","五环"],
        "shanghai":["静安区","浦东新区"]
    },
    "car":["bmw","benz","audi","byd"],
    "pets":[
        { "name":"xiaohei","type":"dog"},
        { "name":"xiaobai","type":"cat"},
        { "name":"xiaofen","type":"cat"},
        { "name":"xiaolan","type":"dog"},
    ]
}

print(jsonpath.jsonpath(jsona,"$.pets[0].type"))
print(jsonpath.jsonpath(jsona, "$.shanghai"))
print(jsonpath.jsonpath(jsona, "$..pets"))
print(jsonpath.jsonpath(jsona,"$..name"))
# 嵌套n层也能取到所有key的值,其中：“$”表示最外层的{}，“..”表示模糊匹配,当传入不存在的key时,程序会返回false

"""
运行结果:

['dog']
False
[[{'name': 'xiaohei', 'type': 'dog'}, {'name': 'xiaobai', 'type': 'cat'}, {'name': 'xiaofen', 'type': 'cat'}, {'name': 'xiaolan', 'type': 'dog'}]]
['xiaohei', 'xiaobai', 'xiaofen', 'xiaolan']
"""