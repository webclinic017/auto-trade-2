import requests
import time

post_url = "http://localhost:5000"
post_result = requests.post(post_url, data={'x': 2})
job_id = post_result.content
print(job_id)

time.sleep(1)

get_url = "http://localhost:5000/result/{}".format(job_id)
get_result = requests.get(get_url)
print(get_result.content)