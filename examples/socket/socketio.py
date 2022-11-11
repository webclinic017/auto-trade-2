import socketio
import time


# wiki地址：http://wiki.okjiaoyu.cn/pages/viewpage.action?spaceKey=RJBK&title=ailearn-instruction-svr
def func(token="", uid=0, room=0):
    sio = socketio.Client()
    event = 'my_event'

    @sio.event()
    def my_response(data):
        # handle the message
        # sio.emit('my_event', {"cmd": "joinRoom", "roomId": 8888})
        print(data)

    @sio.event
    def connect():
        print("I'm connected!")

    @sio.event
    def connect_error():
        print("The connection failed!")

    @sio.event
    def disconnect():
        print("I'm disconnected!")

    url = 'ws://192.168.70.220:9009/?EIO=3&transport=websocket&X-AUTH-TOKEN=727362610017734656&type=1'
    # url = url.format(uid=uid, token=token)

    sio.connect(
        url,transports=["websocket"])
    print('my sid is', sio.sid)
    time.sleep(3)
    # 必需进行注册和加入room操作,room等于发布教学活动的activityid
    sio.emit(event, {"cmd": "register", "userId": uid, "role": "T", "deviceVersion": "1.0","s_sid": sio.sid, "token": token})
    sio.emit(event, {"cmd": "joinRoom", "roomId": room})
    time.sleep(3)


if __name__ == '__main__':
    func(token="727362610017734656", uid=61951375269, room=43548)