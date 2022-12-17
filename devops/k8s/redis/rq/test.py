from rq import Queue
from rq.job import Job
from worker import square_function, conn 
import time

q = Queue(connection=conn)

job = q.enqueue_call(square_function, args=(5, ), result_ttl=5000)   # 保存结果5000s
job_id = job.get_id()
print(job_id)

result1 = Job.fetch(job_id, connection=conn)
print(result1.is_finished)

time.sleep(1)  # 等待队列里任务完成

result2 = Job.fetch(job_id, connection=conn)
print(result2.return_value)