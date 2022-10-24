#!-*-encoding:utf-8-*-

import redis
import json
import types
import collections
from threading import Thread
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


"""
"""
pubsub_channel_one = 'task:pubsub:channel:one'
pubsub_channel_two = 'task:pubsub:channel:two'
pubsub_channel_three = 'task:pubsub:channel:three'
channel_lst = [pubsub_channel_one, pubsub_channel_two,pubsub_channel_three]

class Task(object):

    def __init__(self):
        self.rcon = redis.StrictRedis(host="localhost", db=5)
        self.ps = self.rcon.pubsub()
        self.ps.subscribe(*channel_lst)

    def listen_task(self):
        for i in self.ps.listen():
            if i['type'] == 'message':
                print("Task get", i['channel'], i['data'])


class PubSubSever(object):
    """
    发布订阅服务器， 使用 非阻塞的方式+ 进程池实现， 为每个channel的handler 开辟一个进程
    """
    def __init__(self,redis_conn_pool, channel_lst=[], max_worker_num=10, pool_type='proc'):
        self.rcon = redis.Redis(connection_pool=redis_conn_pool)
        # 初始化线程池
        self.process_pool = ProcessPoolExecutor(max_worker_num)  if pool_type=='proc' else ThreadPoolExecutor(max_worker_num)
        self.channel_lst = channel_lst
        self.registed_handler_dic = collections.defaultdict(list)
        self.pubsub = self.rcon.pubsub()

    def init_sub(self):
        self.pubsub.subscribe(*self.channel_lst)

    def regist_handler(self, channel, handler):

        if channel not in self.registed_handler_dic:
            self.pubsub.subscribe(channel)
            self.channel_lst.append(channel)

        self.registed_handler_dic[channel].append(handler)

    def decode_message(self, message):
        return json.loads(message)

    def parse_message(self, message):
        msg = self.decode_message(message)
        return msg['channel'], msg['data']

    def notify(self, channel, data):
        channel = channel.decode('utf-8')
        idx = 0
        for handler in self.registed_handler_dic[channel]:
            if isinstance(handler, types.FunctionType) or hasattr(handler, '__call__'):
                #print("取出handle")
                # 将handler 和数据封装到一个进程任务中
                self.process_pool.submit(handler, data)


    def event_loop(self):
        """
        服务器以非阻塞的方式运行
        :return:
        """
        while True:
            item = self.pubsub.get_message()    # 非阻塞方式
        # for item in self.pubsub.listen():     # 阻塞方式开启循环
            if not item:
                continue
            if item['type'] == 'message':
                print(item)
                #channel,data = self.parse_message(item)
                channel, data = item['channel'], item['data']
                self.notify(channel, data)

    def close(self):
        self.pubsub.close()
        self.rcon.reset()
        self.process_pool.shutdown()

# =================== handle 各种业务 函数 =========================================
interval = 10
def channel_one_handle_one(data):
    """
    :param data:
    :return:
    """
    print("开启进程handle 1 处理channel 1 的信息")
    time.sleep(interval)
    print("返回结果:")
    print(data)
    return

def channel_two_handle_one(data):
    print("开启进程handle 1 处理channel 2 的信息")
    time.sleep(interval)
    print("返回结果:")
    print(data)
    return

def channel_three_handle_one(data):
    print("开启进程handle 1 处理channel 3 的信息")
    time.sleep(interval)
    print("返回结果:")
    print(data)
    return


def channel_one_handle_two(data):
    """
    :param data:
    :return:
    """
    print("开启进程handle 2 处理channel 1 的信息")
    time.sleep(interval)
    print("返回结果:")
    print(data)
    return


def channel_two_handle_two(data):
    print("开启进程handle 2 处理channel 2 的信息")
    time.sleep(interval)
    print("返回结果:")
    print(data)
    return


def channel_three_handle_two(data):
    print("开启进程handle 2 处理channel 3 的信息")
    time.sleep(interval)
    print("返回结果:")
    print(data)
    return

class Channel_one_handler_three(object):
    def __init__(self):
        pass

    def __call__(self, data):
        print("开启进程handle 类 3 处理channel 1 的信息")
        time.sleep(interval)
        print("返回结果:")
        print(data)
        return


class Channel_two_handler_three(object):
    def __init__(self):
        pass

    def __call__(self, data):
        print("开启进程handle 类 3 处理channel 2 的信息")
        time.sleep(interval)
        print("返回结果:")
        print(data)
        return




def run_server():

    # ===================== params ==================================
    host = "localhost"
    port = 6379
    db = 5
    passwd=None

    # 信道
    pubsub_channel_one = 'task:pubsub:channel:one'
    pubsub_channel_two = 'task:pubsub:channel:two'
    pubsub_channel_three = 'task:pubsub:channel:three'

    # =================================================================
    rcon_pool = redis.ConnectionPool(host=host, port=port, db=db, password=passwd)

    mq_server = PubSubSever(rcon_pool, pool_type='th')

    # 为各个信道注册 handler
    mq_server.regist_handler(pubsub_channel_one, channel_one_handle_one)
    mq_server.regist_handler(pubsub_channel_one, channel_one_handle_two)
    mq_server.regist_handler(pubsub_channel_one, Channel_one_handler_three())

    mq_server.regist_handler(pubsub_channel_two, channel_two_handle_one)
    mq_server.regist_handler(pubsub_channel_two, channel_two_handle_two)
    mq_server.regist_handler(pubsub_channel_two, Channel_two_handler_three())


    mq_server.regist_handler(pubsub_channel_three, channel_three_handle_one)
    mq_server.regist_handler(pubsub_channel_three, channel_three_handle_two)

    # 开始订阅各个handler 对应的channel
    mq_server.init_sub()

    try:
        mq_server.event_loop()
    except InterruptedError as e:
        mq_server.close()

if __name__ == '__main__':
    # print('listen task channel')
    # Task().listen_task()
    run_server()