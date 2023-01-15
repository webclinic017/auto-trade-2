import datetime

import chinese_calendar as calendar
from chinese_calendar import is_workday, is_holiday


def is_workdays(date):
    request_date = datetime.date(date.year, date.month, date.day)
    return is_workday(request_date)


def is_holidays(date):
    request_date = datetime.date(date.year, date.month, date.day)
    return is_holiday(request_date)


def is_festival(date):
    request_date = datetime.date(date.year, date.month, date.day)
    on_holiday, holiday_name = calendar.get_holiday_detail(request_date)
    return on_holiday, holiday_name


if __name__ == "__main__":
    today = datetime.datetime.now()
    week = is_workdays(today)
    holiday = is_holidays(today)
    festival = is_festival(today)
    print("week-{}".format(week))
    print("holiday-{}".format(holiday))
    print("festival-{}-{}".format(festival[0], festival[1]))