from rq import Queue
from rq.job import Job
from worker import conn, square_function

from flask import Flask, request

app = Flask(__name__)

q = Queue(connection=conn) # 建立与Redis server的连接并初始化一个队列

@app.route("/", methods=['POST'])
def index():
    x = request.get_data()  # string 类型
    job = q.enqueue_call(square_function, args=(int(x), ), result_ttl=5000)  # 最后的参数为RQ保留结果的时间
    return job.get_id()  # 返回job的id

@app.route('/result/<job_key>', methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn) # 获取根据job_id获取任务的返回值
    if job.is_finished: # 检验是否完成
        return str(job.result), 200
    else:
        return "Wait!", 202

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)