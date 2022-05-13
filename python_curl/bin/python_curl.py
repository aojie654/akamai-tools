# encoding=utf-8

import json
import socket

import requests

# 指定 "基础Headers"
request_headers_base = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31"
}
# "Akamai debug headers 标准模式" 是在包含UA的 "基础Headers" 之内额外添加Pragma
request_headers_akamai_std = request_headers_base.copy()
request_headers_akamai_std["Pragma"] = "akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-get-cache-key, akamai-x-get-true-cache-key,akamai-x-check-cacheable,akamai-x-get-request-id"
# Akamai debug headers 增强模式 是在 Akamai debug headers 标准模式 的 Pragma 内增加 "akamai-x-get-extracted-values"
request_headers_akamai_ext = request_headers_akamai_std.copy()
request_headers_akamai_ext["Pragma"] = "{}, {}".format(request_headers_akamai_std["Pragma"], "akamai-x-get-extracted-values")

# 指定 超时时间为5分钟 (Akamai 默认超时 300s)
request_timeout = 300

# 更改 DNS IP
# 参考: Stack Overflow: How do I specify URL resolution in python's requests library in a similar fashion to curl's --resolve flag?
# https://stackoverflow.com/questions/44374215/how-do-i-specify-url-resolution-in-pythons-requests-library-in-a-similar-fashio

# 初始化 dns_cache 字典
dns_cache = dict()
# 通过传递参数 hostname 和 ip 更新 socket.getaddrinfo()
prv_getaddrinfo = socket.getaddrinfo


def override_dns(hostname, ip):
    """
    更新目标主机名对应的ip

    输入: hostname=主机名, ip=ip
    输出: 无
    """
    dns_cache[hostname] = ip


def new_getaddrinfo(*args):
    """
    生成新的 addrinfo

    输入: hostname=主机名, *args(额外参数)
    输出: prv_getaddrinfo = socket.getaddrinfo
    """
    if args[0] in dns_cache:
        print("将 域名: {} 绑定至 IP: {}".format(args[0], dns_cache[args[0]]))
        return prv_getaddrinfo(dns_cache[args[0]], *args[1:])
    else:
        return prv_getaddrinfo(*args)


socket.getaddrinfo = new_getaddrinfo


if __name__ == '__main__':
    # 说明内容
    readme_text = """
    说明:
    1. Akamai Header 模式:
        n: 无
        请求Header 中不包含 Akamai Debug Pragma Headers

        s: 标准模式
        "Pragma":   "akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-get-cache-key, akamai-x-get-true-cache-key,
                    akamai-x-check-cacheable, akamai-x-get-request-id"

        e: 增强模式
        "Pragma":   "akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-get-cache-key, akamai-x-get-true-cache-key,
                    akamai-x-check-cacheable, akamai-x-get-request-id, akamai-x-get-extracted-values"
    """
    print(readme_text)

    # 获取输入
    input_str = input("请以空格分割, 输入URL, 请求方法, Akamai Header 模式, 服务器IP: ")
    # input_str = "https://dd.jinmu.info GET n 23.50.49.10"
    # input_str = "https://dd.jinmu.info HEAD s 23.50.49.10"
    # input_str = "https://dd.jinmu.info POST e 23.50.49.10"
    # 以空格分割输入, 并获取 请求url, 请求方法, Akamai Header 模式, 服务器 IP
    input_list = input_str.split(" ")
    request_url, request_method, request_akamai_headers_type, request_server_ip = input_list[0], input_list[1], input_list[2], input_list[3]
    request_hostname = request_url.split("/")[2]

    # 初始化session, 更新 hostname 及 ip
    session_tmp = requests.Session()
    override_dns(hostname=request_hostname, ip=request_server_ip)

    # 判断 Akamai Debug Pragma Headers 模式, 采用对应的 request headers
    if request_akamai_headers_type == "e":
        request_headers = request_headers_akamai_ext
        print("Akamai Debug Pragma Headers: 增强模式")
    elif request_akamai_headers_type == "s":
        request_headers = request_headers_akamai_std
        print("Akamai Debug Pragma Headers: 标准模式")
    else:
        request_headers = request_headers_base
        print("Akamai Debug Pragma Headers: 不使用")
    print("")
    # 发起请求
    response_tmp = session_tmp.request(url=request_url, method=request_method, headers=request_headers, timeout=request_timeout)

    # 输出 响应状态吗
    response_tmp_status = response_tmp.status_code
    output_tips = " 响应状态码: {} ".format(response_tmp_status)
    print("{:=^77}\n".format(output_tips))

    # 输出 响应headers
    output_tips = " 响应 Headers "
    response_tmp_headers = json.dumps(dict(response_tmp.headers), ensure_ascii=False, indent=4, sort_keys=True)[1:-1]
    print("{:=^80}\n{}".format(output_tips, response_tmp_headers))

    # 输出 响应内容
    response_tmp_text = response_tmp.text
    if len(response_tmp_text) == 0:
        output_tips = " 没有响应内容! "
        print("{:=^80}\n".format(output_tips))
    else:
        output_tips = " 响应内容 "
        print("{:=^80}\n{}".format(output_tips, response_tmp_text))
