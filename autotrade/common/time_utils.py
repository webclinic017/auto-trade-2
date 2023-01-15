import datetime
import time

def split_hour_minutes(check_time: str):
    hour = int(check_time.split(':')[0])
    minutes = int(check_time.split(':')[1])
    return hour, minutes

def after_query_time(check_time: str) -> bool:
    ret = False
    cur_time = time.strftime('%H:%M', time.localtime())
    cur_hr, cur_minutes = split_hour_minutes(cur_time)
    check_hr, check_minutes = split_hour_minutes(check_time)
    if cur_hr > check_hr:
        ret = True
    if cur_hr == check_hr:
        if cur_minutes >= check_minutes:
            ret = True
    return ret

def validate(date_text):
    try:
        datetime.datetime.strptime(str(date_text), '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")