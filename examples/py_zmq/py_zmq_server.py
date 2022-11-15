import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5411")

while True:
    message={'name':'yunjinqi','time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())}
    print(message)
    socket.send_string(str(message))
    time.sleep(1)