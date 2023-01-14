import json

"""

"""

obj ={
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

json_obj = json.dumps(obj)
print(json_obj)

load_obj = json.load(json_obj)
print(load_obj)
