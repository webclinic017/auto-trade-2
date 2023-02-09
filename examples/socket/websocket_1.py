import websocket
from websocket import WebSocketApp

try:
    import thread
except ImportError:
    import _thread as thread
import time


class Test(object):
    def __init__(self):
        super(Test, self).__init__()
        self.url = "ws://echo.websocket.org/"
        self.ws = None

    def on_message(self, message):
        print("####### on_message #######")
        print("message：%s" % message)

    def on_error(self, error):
        print("####### on_error #######")
        print("error：%s" % error)

    def on_close(self):
        print("####### on_close #######")

    def on_ping(self, message):
        print("####### on_ping #######")
        print("ping message：%s" % message)

    def on_pong(self, message):
        print("####### on_pong #######")
        print("pong message：%s" % message)

    def on_open(self):
        print("####### on_open #######")

        thread.start_new_thread(self.run, ())

    def run(self, *args):
        while True:
            time.sleep(1)
            input_msg = input("输入要发送的消息（ps：输入关键词 close 结束程序）:\n")
            if input_msg == "close":
                self.ws.close()  # 关闭
                print("thread terminating...")
                break
            else:
                self.ws.send(input_msg)

    def start(self):
        websocket.enableTrace(True)  # 开启运行状态追踪。debug 的时候最好打开他，便于追踪定位问题。

        self.ws = WebSocketApp(self.url,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        # self.ws.on_open = self.on_open  # 也可以先创建对象再这样指定回调函数。run_forever 之前指定回调函数即可。

        self.ws.run_forever()


if __name__ == '__main__':
    Test().start()