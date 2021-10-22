# encoding=utf-8

from datetime import datetime, timedelta


# 格式 %Y%m%d %H%M
time_format = "%Y/%m/%d %H:%M"
time_start_str = input("开始时间: ")
time_start_datetime = datetime.strptime(time_start_str, time_format)
time_end_str = input("结束时间: ")
time_end_datetime = datetime.strptime(time_end_str, time_format)

time_delta = time_end_datetime - time_start_datetime
time_delta_seconds = time_delta.total_seconds()

if time_delta_seconds % 60 < 30:
    time_delta_minutes = time_delta_seconds // 60
else:
    time_delta_minutes = time_delta_seconds // 60 + 1

if time_delta_seconds % 3600 < 1800:
    time_delta_hours = time_delta_seconds // 3600 + 0.5
else:
    time_delta_hours = time_delta_seconds // 3600 + 1

result_text = "相差秒: {}\n相差分钟: {}\n耗费工时: {}".format(time_delta_seconds, time_delta_minutes, time_delta_hours)

print(result_text)
