# encoding=utf-8

"""
cip(Check IP) 的 Python3 版本
"""

import argparse
import json
import re
import sys
from configparser import ConfigParser
from pathlib import Path

import dns.resolver
import requests
from akadata import EdgeScape

# 默认设置
config_filename = "config.ini"
config_path = Path(__file__).parent.joinpath(config_filename)
config_parser = ConfigParser()
config_parser.read(config_path)
config_stanza = "DEFAULT"
config_default = config_parser[config_stanza]
server_timeout = eval(config_default["timeout"])

# 初始化 cip服务器信息
config_stanza = "EDGESCAPE"
config_edgescape = config_parser[config_stanza]
server_es = config_edgescape["server"]
server_port = eval(config_edgescape["port"])

# 初始化 DNS
server_dns = str()

# 在这里定义要输出的字段
list_keys_return = [
    "country_code",
    "region_code",
    "city",
    "network",
    "company",
    "timezone",
    "default_answer"
]


def cip_direct(inputs):
    """
    cip 输入为直接输入IP或域名时的处理流程
    """

    # 将列表中的元素依次输出
    for input in inputs:
        result_cip_list = cip_process(input)
        for result_cip in result_cip_list:
            print(result_cip)

    return


def cip_domain(domain):
    """
    Domain To Location 查询
    """

    # 获取域名对应解析的IP列表
    ip_list = domain_resolve(domain=domain)
    # 初始化域名对应IP查询结果列表
    cip_list_domain = list()
    # 初始化域名查询开始和结束信息
    domain_info = "{:=^54}".format(" {:} ".format(domain))
    # 将提示信息添加至结果集内
    cip_list_domain.append(domain_info)
    # 遍历ip列表, 调用cip_ip, 并将结果追加至结果列表
    for ip_list_elem in ip_list:
        # 判断是否存在异常
        if ip_list_elem.startswith("Exception: "):
            # 如果是, 结果为该异常信息
            result_cip = ip_list_elem.split(": ")[1]
        else:
            # 否则调用 cip_ip 进行单 IP 信息查询
            result_cip = cip_ip(ip=ip_list_elem)
        # 追加至结果集内
        cip_list_domain.append(result_cip)
    # 将提示信息添加至结果集内
    cip_list_domain.append(domain_info)

    return cip_list_domain


def cip_file(files):
    """
    cip 输入为文件时的处理流程
    """

    # 若输入包含 -f 参数, 则输入为文件列表
    for file in files:
        # 使用 file_reader 获取文件内容后生成列表
        inputs = file_reader(file)
        result_cip_list = list()
        # 当列表长度不为0时, 将文件内容列表作为输入调用cip_process, 获取结果后写入文件
        if len(inputs) != 0:
            for input in inputs:
                result_cip_list = result_cip_list + cip_process(input=input)
            file_writer(file=file, result_cip_list=result_cip_list)
        else:
            pass

    return


def cip_ip(ip):
    """
    查询单个IP 的主要函数
    """

    try:
        result_final = ip + ": [ "
        es_client = EdgeScape(host=server_es, port=server_port)
        result_lookup = es_client.ip_lookup(ip, timeout=server_timeout)
        for key_tmp in list_keys_return:
            if key_tmp in result_lookup.keys():
                if key_tmp == "default_answer":
                    if result_lookup[key_tmp] == True:
                        result_lookup[key_tmp] = "Y"
                    else:
                        result_lookup[key_tmp] = "N"
                result_final = result_final + key_tmp + ": " + result_lookup[key_tmp]
                if key_tmp != list_keys_return[-1]:
                    result_final = result_final + ", "
                else:
                    result_final = result_final + " ]"
            else:
                continue
    except Exception as identifier:
        tip_error = "Request error of {:}: ".format(ip)
        result_final = "{:}{:}".format(tip_error, identifier)
    finally:
        return result_final


def cip_process(input):
    """
    cip 的通用处理流程
    """

    # 创建结果集列表, 统一 单IP 和 域名(多IP) 查询结果格式
    result_cip_list = list()

    input_type = input_type_detection(input=input)
    if (input_type == "invalid"):
        # 不属于 ip或域名 时, 查询结果为错误提示
        result_cip_list.append("{:}: 参数有误, 无效的ip或域名".format(input))
    elif (input_type == "ipv4") or (input_type == "ipv6"):
        # 当 input_type是 ipv4 或 ipv6, 调用ip查询函数
        result_cip_list.append(cip_ip(ip=input))
    elif (input_type == "domain"):
        # 当 input_type 是 域名类型时, 调用域名查询函数
        result_cip_list = result_cip_list + cip_domain(domain=input)

    return result_cip_list


def domain_resolve(domain):
    """
    域名解析
    """
    # 创建 resolver对象
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.lifetimeout = 1
    # 当DNS服务器不为空时, 使用传入的DNS服务器
    if server_dns != "":
        resolver.nameservers = server_dns
    else:
        pass
    # 初始化ip列表
    ip_list = list()
    # 将解析出的所有结果逐一添加到ip列表结果里
    try:
        for rrset_tmp in resolver.resolve(domain).rrset:
            if rrset_tmp.address != "":
                ip_list_elem = rrset_tmp.address
    except Exception as exception:
        ip_list_elem = "Exception: {:}".format(exception)
    finally:
        ip_list.append(ip_list_elem)
    return ip_list


def file_reader(file):
    """
    根据文件读取内容生成文件列表
    """

    file_content_list = list()
    # 当文件存在时读取文件内容
    file_obj = Path(file)
    if Path.exists(file_obj):
        # 打开文件, 读取内容后去掉两端多余字符, 然后以回车分割
        file_object = open(file, encoding="utf-8", mode="r")
        file_content = file_object.read().strip()
        file_object.close()
        file_content_list = file_content.split("\n")
    else:
        # 文件不存在时输出提醒
        print("文件: {:} 不存在!".format(file))

    return file_content_list


def file_writer(file, result_cip_list):
    """
    将查询结果列表列表追加至文本后
    """

    # 以追加模式打开文件,
    file_object = open(file, encoding="utf-8", mode="a")
    # 添加空行 和 提示信息
    result_cip_list = ["", "", "以上内容的查询结果如下:"] + result_cip_list
    # 将结果集中的内容依次添加换行后写入文件并关闭文件
    for content_tmp in result_cip_list:
        file_object.writelines("{:}\n".format(content_tmp))
        file_object.flush()
    file_object.close()
    # 输出处理结果提示
    print("文件: {:} 内容查询完成, 查询结果已追加至源文件内".format(file))

    return


def input_type_detection(input):
    """
    判断 对象类型
    """

    # 初始化 ipv4, ipv6, 域名的对应正则匹配表达式
    re_ipv4 = "(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))"
    re_ipv6 = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    re_domain = "((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}"

    # 根据正则匹配判断 输入内容的 类型, 并保存至 input_type
    input_type = "invalid"
    if re.match(re_ipv4, input):
        input_type = "ipv4"
    elif re.match(re_ipv6, input):
        input_type = "ipv6"
    elif re.match(re_domain, input):
        input_type = "domain"
    else:
        pass

    # 返回 input_type 类型
    return input_type


def get_info():
    """
    获取 info.json 内容
    """

    file_info_name = "info.json"
    file_info_path = Path(__file__).parent.joinpath(file_info_name)

    # 当文件存在时读取文件内容
    if Path.exists(file_info_path):
        # 打开文件, 读取内容后关闭文件
        file_object = open(file_info_path, encoding="utf-8", mode="r")
        file_info_json = json.loads(file_object.read())
        file_object.close()
    else:
        # 文件不存在时输出提示
        print("文件: {:} 不存在!".format(file_info_path))

    return file_info_json


def get_log_update(args):
    """
    返回 版本日志
    """

    # 获取版本信息
    log_info_json = get_info()["log"]
    log_update_pretty = str()

    if args.l:
        version = get_version_current()
        log_update_pretty = "v{:}".format(version)
        for log_update in log_info_json[version]:
            log_update_pretty = "{:}\n  - {:}".format(log_update_pretty, log_update)
    else:
        for version in log_info_json.keys():
            log_update_pretty = "{:}\nv{:}".format(log_update_pretty, version)
            for log_update in log_info_json[version]:
                log_update_pretty = "{:}\n  - {:}".format(log_update_pretty, log_update)
        log_update_pretty = log_update_pretty[1:]

    return log_update_pretty


def get_version(args):
    """
    根据参数 -v 或 --version 获取版本
    """

    file_info_json = get_info()

    if args.v:
        version = get_version_current()
    else:
        version = file_info_json["version"]
        version = json.dumps(version, ensure_ascii=False, indent=2)

    return version


def get_version_current():
    """
    获取当前版本号
    """

    file_info_json = get_info()
    version = file_info_json["version"]["Version"]

    return version


def json_pretty(obj):

    return json.dumps(obj=obj, ensure_ascii=False, indent=2)


def update():
    """
    检查脚本更新
    """

    # 初始化版本信息, 转换为数字
    version_current = get_version_current()
    version_current_int = int(version_current.replace(".", ""))
    version_remote = str()
    # 初始化 cip文件 的路径
    path_cip = __file__
    filename_info = "info.json"
    path_info = Path(__file__).parent.joinpath(filename_info)

    # 初始化 cip更新服务器 及 url
    server_stanza = "UPDATE"
    config_update = config_parser[server_stanza]
    server_update = config_update["server"]
    url_path = config_update["path"]
    filename_cip = config_update["filename_cip"]
    filename_info = config_update["filename_info"]
    url_cip = "https://{:}{:}{:}".format(server_update, url_path, filename_cip)
    url_info = "https://{:}{:}{:}".format(server_update, url_path, filename_info)

    # 创建对象获取远端信息
    info_response = requests.request(method="GET", url=url_info)
    # 当状态码存在且为200时:
    if ((info_response.status_code is not None) and (info_response.status_code == 200)):
        # 从远端信息中去除 版本号
        info_remote_obj = info_response.json()
        version_remote = info_remote_obj["version"]["Version"]
        version_remote_int = int(version_remote.replace(".", ""))
        tip_update = {
            "cip 文件路径": "{:}".format(path_cip),
            "cip 更新 URL": "{:}".format(url_cip),
            "info 文件路径": "{:}".format(path_info),
            "info 更新 URL": "{:}".format(url_info),
            "当前版本": "{:}".format(version_current),
            "cip 远端版本": "{:}".format(version_remote),
        }
        for key in tip_update.keys():
            print("{:}: {:}".format(key, tip_update[key]))

        if version_remote_int > version_current_int:
            # 当远端版本高于当前版本时, 进行文件更新
            result_response_cip = requests.request(method="GET", url=url_cip)
            if ((result_response_cip.status_code is not None) and (result_response_cip.status_code == 200)):
                # 文件请求状态正常时, 输出更新开始状态
                print("请求远端cip文件正常, 开始更新...")
                # 更新 cip 文件内容
                cip_obj = open(file=path_cip, encoding="utf-8", mode="w", errors="ignore")
                cip_obj.write(result_response_cip.text)
                cip_obj.flush()
                cip_obj.close()
                # 更新 info 文件内容
                info_obj = open(file=path_info, encoding="utf-8", mode="w", errors="ignore")
                info_obj.write(info_response.text)
                info_obj.flush()
                info_obj.close()
                # 输出更新日志
                args.l = True
                log_update = get_log_update(args)
                print("\n更新日志: {:}\n".format(log_update))
                # 输出更新完成状态
                print("更新完成啦, 看看写代码的这次又新增了多少个bug~")
            elif (result_response_cip.status_code is not None):
                print("Oops! 请求远端cip文件出错: 未收到请求响应码")
            else:
                print("Oops! 获取远端版本出错: 响应码: {:}".format(result_response_cip.status_code))
        elif version_remote == version_current:
            # 版本一致时提示无需更新
            print("和远端版本一样咯, 没必要更新啦~")
        else:
            # 远端版本低于当前版本时
            print("你本地的版本居然比远端版本还要高? 确定你没有偷偷改掉本地版本吗?")
    elif (info_response.status_code is None):
        print("Oops! 获取远端版本出错: 未收到请求响应码!")
    else:
        print("Oops! 获取远端版本出错: 状态码为: {:}".format(info_response.status_code))


if __name__ == "__main__":
    # _DEBUG_FLAG
    # sys.argv = [__file__, "-i", "1.1.1.1"]
    # sys.argv = [__file__, "-i", "1.1.1.1", "www.akamai.com"]
    # sys.argv = [__file__, "-i", "1.1.1.1", "www.akamai.com", "-d", "8.8.8.8"]
    # sys.argv = [__file__, "-f", "/Users/sao/Downloads/iptest1.txt"]
    # sys.argv = [__file__, "-f", "/Users/sao/Downloads/iptest1.txt", "-d", "8.8.8.8"]
    # sys.argv = [__file__, "-f", "/Users/sao/Downloads/iptest1.txt", "/Users/sao/Downloads/iptest2.txt"]
    # sys.argv = [__file__, "-f", "/Users/sao/Downloads/iptest1.txt", "/Users/sao/Downloads/iptest2.txt", "-d", "8.8.8.8"]
    # sys.argv = [__file__, "-l"]
    # sys.argv = [__file__, "--log"]
    # sys.argv = [__file__, "-u"]
    # sys.argv = [__file__, "-v"]
    # sys.argv = [__file__, "--version"]
    # print(sys.argv)

    # 创建 参数解析对象
    arg_parser = argparse.ArgumentParser(
        prog="cip",
        description="将输入的 IP 或域名通过 Akamai Edgescape 转化为地理位置信息.",
    )

    # 添加 input_type, dns, 文件 及 更新参数
    arg_parser.add_argument("-i", "--input", nargs="+", help="输入, 默认为 IP 或域名, 可输入多个, 以空格分割.")
    arg_parser.add_argument("-d", "--dns", nargs="+", help="在输入域名时指定 DNS服务器, 可输入多个, 以空格分割. 未指定时默认使用 Local DNS.")
    arg_parser.add_argument("-f", "--file", nargs="+", help="指定文件作为输入, 并将结果追加至该文件内.")
    # 与 lib -h 项冲突, 暂不使用
    # arg_parser.add_argument("-h", "--help", help="显示该帮助文本后退出", dest="", action="store_true")
    arg_parser.add_argument("-l", help="查看当前更新日志.", action="store_true")
    arg_parser.add_argument("--log", help="查看所有更新日志.", action="store_true")
    arg_parser.add_argument("-u", "--update", help="更新 cip.", action="store_true")
    arg_parser.add_argument("-v", help="查看 cip 的版本信息.", action="store_true")
    arg_parser.add_argument("--version", help="查看 cip 的版本详细信息.", action="store_true")

    # 解析参数
    args = arg_parser.parse_args()
    if (args.input or args.file):
        # _DEBUG_FLAG
        # print("参数详情: {:}".format(args))
        tip_msg = "{:} SERVER: {:}:{:}".format("="*5, server_es, server_port)
        print(tip_msg)

        # 使用输入时指定的dns服务器
        if args.dns:
            # 当DNS服务器不为空时, 使用传入的DNS服务器
            server_dns = args.dns
            tip_dns = server_dns
        else:
            tip_dns = "Local DNS"
        tip_dns_msg = "DNS: {:}".format(tip_dns)
        tip_msg = "{:} {:}".format("="*5, tip_dns_msg)
        print(tip_msg)

        if args.input:
            # 存在 -i 时, 将 输入内容 作为输入调用 cip_direct 进行直接输出
            cip_direct(inputs=args.input)
        elif args.file:
            # 存在 -f 时, 将 文件列表 作为输入调用 cip_file 读取并写入文件
            cip_file(files=args.file)
        else:
            print("输入有误, 输入参数至少需要 -i 和 -f 的其中一个")

        # 显示运行结束提示
    elif (args.l or args.log):
        # 当参数中包含 -l 或 --log 时输出更新日志
        print(get_log_update(args))
    elif args.update:
        # 当参数中包含 -u 或 --update 时检查更新
        update()
    elif (args.v or args.version):
        # 当参数中包含 -v 或 --version 时输出版本信息
        print(get_version(args))
    else:
        # 若未传入任何正确参数, 显示帮助
        arg_parser.print_help()
