#!-*-encoding:utf-8-*-

import redis
import random
import logging
import random

from flask import Flask, redirect

app = Flask(__name__)

rcon = redis.StrictRedis(host='localhost', db=5)
prodcons_queue_one = 'task:prodcons:queue:one'
prodcons_queue_two = 'task:prodcons:queue:two'
prodcons_queue_three = 'task:prodcons:queue:three'

pubsub_channel_one = 'task:pubsub:channel:one'
pubsub_channel_two = 'task:pubsub:channel:two'
pubsub_channel_three = 'task:pubsub:channel:three'

queue_lst = [prodcons_queue_one, prodcons_queue_two, prodcons_queue_three]
channel_lst = [pubsub_channel_one, pubsub_channel_two, pubsub_channel_three]

@app.route("/")
def index():
    html = """   
    <br>
    <center><h3>Redis Message Queue</h3>
    <br>
    <a href="/prodcons">生产消费者模式</a>
    <br>
    <br>
    <a href="/pubsub">发布订阅者模式</a>
    """

    return html

@app.route('/prodcons')
def prodcons():

    queue_name = random.choice(queue_lst)
    for i in range(10):
        elem = random.randrange(10)
        rcon.lpush(queue_name, elem)
    logging.info("lpush {} -- {}".format(queue_name, elem))
    return redirect('/')

@app.route('/pubsub')
def pubsub():
    ps = rcon.pubsub()
    channel = random.choice(channel_lst)
    ps.subscribe(channel)
    elem = random.randrange(10)
    rcon.publish(channel, elem)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)