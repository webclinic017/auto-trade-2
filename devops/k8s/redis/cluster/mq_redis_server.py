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

prodcons_queue_one = 'task:prodcons:queue:one'
prodcons_queue_two = 'task:prodcons:queue:two'
prodcons_queue_three = 'task:prodcons:queue:three'

queue_lst = [prodcons_queue_one, prodcons_queue_two, prodcons_queue_three]

class Task(object):

    def __init__(self):
        self.rcon = redis.StrictRedis(host="localhost", db=5)
        self.queue_lst = queue_lst

    def listen_task(self):
        while True:
            channel,task = self.rcon.blpop(self.queue_lst, 0)
            print("Task get",channel, task)



class MQServer(object):

    def __init__(self, conn_pool,channel_lst=[], batch_size=5, max_worker_num=10, pool_type='proc'):
        self.rcon = redis.Redis(connection_pool=conn_pool)
        self.process_pool = ProcessPoolExecutor(max_worker_num) if pool_type == 'proc' else ThreadPoolExecutor(
            max_worker_num)
        self.batch_size = batch_size
        self.channel_lst = channel_lst
        self.registed_handler_dic = collections.defaultdict(list)

    def regist_handler(self, channel, handler):
        if channel not in self.registed_handler_dic:
            self.channel_lst.append(channel)

        self.registed_handler_dic[channel].append(handler)

    def notify(self, channel, payload):
        channel = channel.decode('utf-8') if not isinstance(channel, str) else channel
        idx = 0
        for handler in self.registed_handler_dic[channel]:
            if isinstance(handler, types.FunctionType) or hasattr(handler, '__call__'):
                #print("取出handle")
                # 将handler 和数据封装到一个进程任务中
                self.process_pool.submit(handler, payload)

    def event_loop(self):
        """
        服务器以阻塞的方式运行
        :return:
        """
        while True:
            channel,payload = self.rcon.blpop(self.channel_lst)    # 阻塞方式
            #print(channel, payload)
            if not payload:
                continue
            self.notify(channel, payload)

    def batch_event_loop(self):
        """
        使用批次处理
        :return:
        """
        while True:
            for channel in self.channel_lst:
                cur_queue = self.rcon.lrange(channel, 0, self.batch_size-1)

                cur_queue_len = len(cur_queue)
                if cur_queue_len == 0:
                    continue

                print("当前取出队列的长度为: %d" % cur_queue_len)
                # 从队列中移除当前处理的数据
                self.rcon.ltrim(channel,cur_queue_len, -1)

                payload = cur_queue
                self.notify(channel, payload)


    def close(self):
        self.pubsub.close()
        self.rcon.reset()
        self.process_pool.shutdown()

# 这里定义handler 函数和可执行类
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
    passwd = None

    # 信道
    prodcons_queue_one = 'task:prodcons:queue:one'
    prodcons_queue_two = 'task:prodcons:queue:two'
    prodcons_queue_three = 'task:prodcons:queue:three'

    # =================================================================
    rcon_pool = redis.ConnectionPool(host=host, port=port, db=db, password=passwd)

    mq_server = MQServer(rcon_pool, pool_type='th')

    mq_server.regist_handler(prodcons_queue_one, channel_one_handle_one)
    mq_server.regist_handler(prodcons_queue_one, channel_one_handle_two)
    # mq_server.regist_handler(prodcons_queue_one, Channel_one_handler_three())

    mq_server.regist_handler(prodcons_queue_two, channel_two_handle_one)
    mq_server.regist_handler(prodcons_queue_two, channel_two_handle_two)
    # mq_server.regist_handler(prodcons_queue_two, Channel_two_handler_three())

    mq_server.regist_handler(prodcons_queue_three, channel_three_handle_one)
    mq_server.regist_handler(prodcons_queue_three, channel_three_handle_two)

    try:
        # mq_server.event_loop()
        mq_server.batch_event_loop()
    except InterruptedError as e:
        mq_server.close()

if __name__ == '__main__':
    # print('listen task queue')
    # Task().listen_task()

    run_server()
