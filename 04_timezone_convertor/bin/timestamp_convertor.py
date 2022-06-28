# encoding=utf-8

from datetime import datetime, timedelta

# 指定 时间的格式
datetime_format = str("%Y/%m/%d %H:%M:%S")


def time_datetime_generator(time_str):
    """
    datetime 生成器

    输入: 符合 "{}" 格式的时间字符串
    """.format(datetime_format)

    # 通过 datetime_format 解析字符串成 datetime 对象
    time_datetime = datetime.strptime(before_time_str, datetime_format)

    return time_datetime


def timezone_timedelta_generator(timezone_str):
    """
    timedelta 生成器

    输入:
    """
    if ":" in timezone_str:
        # 将 时区字符串 以 ":" 分割获取 转换前时区 中的 小时 及 分钟
        timezone_list = timezone_str.split(":")
        timezone_hour, timezone_min = int(timezone_list[0]), int(timezone_list[1])
    else:
        timezone_hour = int(timezone_str)
        timezone_min = 0
    # 生成 timezone 的 timedelta 对象
    timezone_timedelta = timedelta(hours=timezone_hour, minutes=timezone_min)

    return timezone_timedelta


if __name__ == '__main__':
    input_hint = """
    说明:
    1. 时间格式:
        {}. 例如: 2021/09/28 22:55:54
    
    2. 时区格式:
        1. 前位"0"可省略, 例如: +2:00
        2. 正号可省略. 例如: 2:00, 5:30
        3. 在不包含分钟时, 冒号及冒号后分钟可省略. 例如: 2, -3
        4. 合法样例: +01:00, +1:00, +1, 1, -02:00, -2:30, -2
    """.format(datetime_format)
    print(input_hint)

    # 获取 转换前时间, 时区, 以及 转换后的时区
    before_time_str = input("请输入 转换前时间: ")
    before_timezone_str = input("请输入 转换前时区: ")
    after_timezone_str = input("请输入 转换后时区: ")
    # _DEBUG_FLAG
    # before_time_str = "2021/09/28 22:55:54"
    # before_timezone_str = "+08:00"
    # after_timezone_str = "-04:00"

    # 将 转换前时间 转换为 datetime 对象
    before_time_datetime = time_datetime_generator(before_time_str)
    # 获 转换前时间 的 timedelta 对象
    before_timezone_timedelta = timezone_timedelta_generator(timezone_str=before_timezone_str)
    utc_time_datetime = before_time_datetime - before_timezone_timedelta

    # 将 转换后时区 转换为 timedelta
    after_timezone_timedelta = timezone_timedelta_generator(timezone_str=after_timezone_str)
    # 计算 转换后时间
    after_time_datetime = utc_time_datetime + after_timezone_timedelta
    # 格式化 目标时区 时间
    after_time_str = after_time_datetime.strftime(datetime_format)

    # 填充 输出结果
    after_time_result = """
    转换前时区: {}
    转换前时间: {}
    转换后时区: {}
    转换后时间: {}
    """.format(before_timezone_str, before_time_str, after_timezone_str, after_time_str)

    # 输出
    print(after_time_result)
