from redis_queue import RedisQueue
import time

q = RedisQueue('rq')
while 1:
    result = q.get_nowait()
    if not result:
        break
    print("output.py: data {} out of queue {}".format(result, time.strftime("%c")))
    time.sleep(2)