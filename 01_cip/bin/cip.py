# encoding=utf-8

"""
cip(Check IP) with python3
cip(Check IP) 的 python3 版本
"""

import argparse
import json
import re
# !!! DO NOT REMOVE sys FOR WHICH USING TO DEBUG !!!
import sys
from configparser import ConfigParser
from pathlib import Path

import dns.resolver
import requests
from akadata import EdgeScape

# Default settings
# 默认设置
config_filename = "config.ini"
folder_path = Path(__file__).parent
config_path = folder_path.joinpath(config_filename)
config_parser = ConfigParser()
config_parser.read(config_path)
config_stanza = "DEFAULT"
config_default = config_parser[config_stanza]
server_timeout = eval(config_default["timeout"])

# Set the output fields
# 配置需要输出的字段
list_keys_return = eval(config_default["fields"])
# Config to display fields name or not
# 配置是否显示字段名
if config_default["fields_name"].lower() == "off":
    display_field_name = False
else:
    display_field_name = True

# Initiate the server info of EdgeScape Facilitator
# 初始化 Edgescape Facilitator 服务器信息
config_stanza = "EDGESCAPE"
config_edgescape = config_parser[config_stanza]
server_es = config_edgescape["server"]
server_port = eval(config_edgescape["port"])

# Initiate DNS
# 初始化 DNS
server_dns = str()

# Initiate Country Code
# 初始化 国家代码
country_filename = "country.json"
country_path = folder_path.joinpath(country_filename)
country_obj = open(file=country_path, mode="r", encoding="utf-8", errors="ignore")
country_text = country_obj.read()
country_json = json.loads(country_text)
country_obj.close()


def cip_direct(inputs):
    """
    The processing when IP or domain as input directly
    cip 输入为直接输入IP或域名时的处理流程
    """

    # Output the elements
    # 将列表中的元素依次输出
    for input in inputs:
        result_cip_list = cip_process(input)
        for result_cip in result_cip_list:
            print(result_cip)

    return


def cip_domain(domain):
    """
    Domain To Location
    """

    # Resolve the IPs of domain
    # 获取域名对应解析的 IP 列表
    ip_list = domain_resolver(domain=domain)
    # Initiate the result list of queries
    # 初始化域名对应 IP 查询结果列表
    cip_list_domain = list()
    # Initiate the start and finished msg
    # 初始化域名查询开始和结束信息
    domain_info = "{:=^54}".format(" {:} ".format(domain))
    # Then add them to result list
    # 将提示信息添加至结果集内
    cip_list_domain.append(domain_info)
    # Revoke the cip_ip() for every IP of domain and add the result to the list
    # 遍历 ip 列表, 调用 cip_ip(), 并将结果追加至结果列表
    for ip_list_elem in ip_list:
        # Exception or not
        # 判断是否存在异常
        if ip_list_elem.startswith("Exception: "):
            # Exception when result start with "Exception: " that we defined
            # 如果是, 结果为该异常信息
            result_cip = ip_list_elem.split(": ")[1]
        else:
            # Or using cip_ip() to get the result
            # 否则调用 cip_ip() 进行单 IP 信息查询
            result_cip = cip_ip(ip=ip_list_elem)
        # Add them to result list
        # 追加至结果集内
        cip_list_domain.append(result_cip)
    # Add the domain msg to result list
    # 将提示信息添加至结果集内
    cip_list_domain.append(domain_info)

    return cip_list_domain


def cip_file(files):
    """
    cip 输入为文件时的处理流程
    """

    # The input are files when "-f" is included
    # 若输入包含 -f 参数, 则输入为文件列表
    for file in files:
        # Read the file with file_reader() then generate the input list
        # 使用 file_reader() 获取文件内容后生成列表
        inputs = file_reader(file)
        result_cip_list = list()
        # Revoke cip_process() when length of input list is not 0, then append the result list to files
        # 当列表长度不为0时, 将文件内容列表作为输入调用cip_process, 获取结果后追加写入文件
        if len(inputs) != 0:
            for input in inputs:
                result_cip_list = result_cip_list + cip_process(input=input)
            file_writer(file=file, result_cip_list=result_cip_list)
        else:
            pass

    return


def cip_ip(ip):
    """
    Query of sinegle IP
    查询单个IP 的主要函数
    """

    try:
        result_final = ip + ": [ "
        es_client = EdgeScape(host=server_es, port=server_port)
        result_lookup = es_client.ip_lookup(ip, timeout=server_timeout)
        # print(result_lookup)
        for key_tmp in list_keys_return:
            if key_tmp in result_lookup.keys():
                value_tmp = result_lookup[key_tmp]
                if (key_tmp == "country_code") and (value_tmp in country_json.keys()):
                    key_tmp = "country"
                    value_tmp = country_json[value_tmp]
                if key_tmp == "default_answer":
                    if value_tmp == True:
                        value_tmp = "Y"
                    else:
                        value_tmp = "N"
                if display_field_name:
                    result_final = result_final + key_tmp + ": " + value_tmp
                else:
                    result_final = result_final + value_tmp
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
    Decide the input is IP or domain
    根据输入判断 ip 或域名
    """

    # Create the reulst list including the result of single IP and domain(multiple IPs)
    # 创建结果集列表, 统一 单IP 和 域名(多IP) 查询结果格式
    result_cip_list = list()

    input_type = input_type_detection(input=input)
    if (input_type == "invalid"):
        # Error msg when input is a invalid IP or domain
        # 不属于 ip或域名 时, 查询结果为错误提示
        result_cip_list.append("{:}: Invalid IP or domain.".format(input))
    elif (input_type == "ipv4") or (input_type == "ipv6"):
        # revoke cip_ip() when input_type is ipv4 or ipv6
        # 当 input_type是 ipv4 或 ipv6, 调用ip查询函数
        result_cip_list.append(cip_ip(ip=input))
    elif (input_type == "domain"):
        # revoke cip_domain() when input_type is domain
        # 当 input_type 是 域名类型时, 调用域名查询函数
        result_cip_list = result_cip_list + cip_domain(domain=input)

    return result_cip_list


def domain_resolver(domain):
    """
    Domain resolver
    域名解析
    """
    # Create the object of resolver
    # 创建 resolver 对象
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.lifetimeout = 1
    # Use the input as DNS server when input is not None
    # 当 DNS 服务器不为空时, 使用传入的DNS服务器
    if server_dns != "":
        resolver.nameservers = server_dns
    else:
        pass
    # Initiate the IP list
    # 初始化 IP 列表
    ip_list = list()
    # Add every IP to IP list
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
    Read file add generate the content list
    根据文件读取内容生成文件列表
    """

    file_content_list = list()
    # Read file when it exist
    # 当文件存在时读取文件内容
    file_obj = Path(file)
    if Path.exists(file_obj):
        # Remove the blank string at starting and tailing then split with "\n"
        # 打开文件, 读取内容后去掉两端多余字符, 然后以回车分割
        file_object = open(file, encoding="utf-8", mode="r")
        file_content = file_object.read().strip()
        file_object.close()
        file_content_list = file_content.split("\n")
    else:
        # Output the file not exist msg
        # 文件不存在时输出提醒
        print("ERROR: No such file: {:}".format(file))

    return file_content_list


def file_writer(file, result_cip_list):
    """
    Append the results to file
    将查询结果列表列表追加至文本后
    """

    # Open file with append mode
    # 以追加模式打开文件
    file_object = open(file, encoding="utf-8", mode="a")
    # Add blank row and msg
    # 添加空行 和 提示信息
    result_cip_list = ["", "", "Here are the queries result:"] + result_cip_list
    # Add the result list to file, then close the file
    # 将结果集中的内容依次添加换行后写入文件并关闭文件
    for content_tmp in result_cip_list:
        file_object.writelines("{:}\n".format(content_tmp))
        file_object.flush()
    file_object.close()
    # Output the processing msg
    # 输出处理结果提示
    print("Quries of file: {:} done, all the results are append to the file.".format(file))

    return


def input_type_detection(input):
    """
    Decide the input type
    判断 对象类型
    """

    # Initiate the regex of IPv4, IPv6 and domain
    # 初始化 ipv4, ipv6, 域名的对应正则匹配表达式
    re_ipv4 = "(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))"
    re_ipv6 = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    re_domain = "((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}"

    # Decide the input type by regex as input_type
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

    return input_type


def get_info():
    """
    Get the content of info.json
    获取 info.json 内容
    """

    file_info_name = "info.json"
    file_info_path = Path(__file__).parent.joinpath(file_info_name)

    # Read the content if file exist
    # 当文件存在时读取文件内容
    if Path.exists(file_info_path):
        # Open the file, read and close
        # 打开文件, 读取内容后关闭文件
        file_object = open(file_info_path, encoding="utf-8", mode="r")
        file_info_json = json.loads(file_object.read())
        file_object.close()
    else:
        # Output the msg when file not exist
        # 文件不存在时输出提示
        print("ERROR: No such file: {:}".format(file_info_path))

    return file_info_json


def get_log_update(args):
    """
    Return the version log
    返回 版本日志
    """

    # Get version info
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
    Get version info decided on the option -v or --version
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
    Get the current version
    获取当前版本号
    """

    file_info_json = get_info()
    version = file_info_json["version"]["Version"]

    return version


def json_pretty(obj):

    return json.dumps(obj=obj, ensure_ascii=False, indent=2)


def update():
    """
    Check update of CIP
    检查脚本更新
    """

    # Initiate the version and convert to num
    # 初始化版本信息, 转换为数字
    version_current = get_version_current()
    version_current_int = int(version_current.replace(".", ""))
    version_remote = str()
    # Initiate the path of cip file
    # 初始化 cip文件 的路径
    path_cip = __file__
    filename_info = "info.json"
    path_info = Path(__file__).parent.joinpath(filename_info)

    # Initiate the update server and url of cip
    # 初始化 cip 更新服务器 及 url
    server_stanza = "UPDATE"
    config_update = config_parser[server_stanza]
    server_update = config_update["server"]
    url_path = config_update["path"]
    filename_cip = config_update["filename_cip"]
    filename_info = config_update["filename_info"]
    url_cip = "https://{:}{:}{:}".format(server_update, url_path, filename_cip)
    url_info = "https://{:}{:}{:}".format(server_update, url_path, filename_info)

    tip_update = {
        "info path": "{:}".format(path_info),
        "info URL": "{:}".format(url_info),
        "cip path": "{:}".format(path_cip),
        "cip URL": "{:}".format(url_cip),
        "cip current version": "{:}".format(version_current),
    }
    for key in tip_update.keys():
        print("{:}: {:}".format(key, tip_update[key]))

    try:
        # Create request object
        # 创建对象获取远端信息
        info_response = requests.request(method="GET", url=url_info)
        # When request success and the status code is 200
        # 当请求正常且状态码为200时
        if (info_response.status_code == 200):
            # Get the version of remote info
            # 从远端信息中获取 版本号
            info_remote_obj = info_response.json()
            version_remote = info_remote_obj["version"]["Version"]
            version_remote_int = int(version_remote.replace(".", ""))
            print("cip retmote version: {:}".format(version_remote))

            if version_remote_int > version_current_int:
                # Update cip when remote newer than current
                # 当远端版本高于当前版本时, 进行文件更新
                result_response_cip = requests.request(method="GET", url=url_cip)
                if (result_response_cip.status_code == 200):
                    # Output success
                    # 文件请求状态正常时, 输出更新开始状态
                    print("Request cip success, strating update...")
                    # Update cip file
                    # 更新 cip 文件内容
                    cip_obj = open(file=path_cip, encoding="utf-8", mode="w", errors="ignore")
                    cip_obj.write(result_response_cip.text)
                    cip_obj.flush()
                    cip_obj.close()
                    # Update info file
                    # 更新 info 文件内容
                    info_obj = open(file=path_info, encoding="utf-8", mode="w", errors="ignore")
                    info_obj.write(info_response.text)
                    info_obj.flush()
                    info_obj.close()
                    # Output update log
                    # 输出更新日志
                    args.l = True
                    log_update = get_log_update(args)
                    print("\nUpdate log: {:}\n".format(log_update))
                    # Output update status
                    # 输出更新完成状态
                    tip_update = "Update finished. Let's have a try about how many bugs are added in this update~"
                else:
                    tip_update = "Oops! Received status code: {:} when request to {:}".format(result_response_cip.status_code, url_cip)
                print()
                print(tip_update)
            elif version_remote == version_current:
                # No need update when local version equals remote version
                # 版本一致时提示无需更新
                print()
                print("We are using the same version of remote, so there is no need to update~")
            else:
                # Output msg when local version newer than remote one
                # 远端版本低于当前版本时
                print()
                print("Emmm... I think maybe you edited your local version which is newer than remote one?")
        else:
            print()
            print("Oops! Received status code: {:} when request to {:}".format(info_response.status_code, url_info))
    except Exception as exception:
        print()
        print("Oops! Error occurs when request to {:}: {:}".format(url_info, exception))


if __name__ == "__main__":
    # _DEBUG_FLAG
    sys.argv = [__file__, "-i", "1.1.1.1"]
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

    # Create the object of parser.
    # 创建 参数解析对象
    arg_parser = argparse.ArgumentParser(
        prog="cip",
        description="IP2Location with EdgeScape Facilitator.",
    )

    # Add argument of input, dns, files and update
    # 添加 input, dns, 文件 及 更新参数
    arg_parser.add_argument("-i", "--input", nargs="+", help="Inputs. IP or Domain by default. Split with space when you input multiple values.")
    arg_parser.add_argument("-d", "--dns", nargs="+", help="DNS server which you want to use. Local DNS by default. Split with space when you input multiple values.")
    arg_parser.add_argument("-f", "--file", nargs="+", help="Input file path as input. Split with space when you input multiple values.")
    # Conflict with default "-h", do not use at now.
    # 与 lib -h 项冲突, 暂不使用
    # arg_parser.add_argument("-h", "--help", help="Show the help message", dest="", action="store_true")
    arg_parser.add_argument("-l", help="Show the log of current version", action="store_true")
    arg_parser.add_argument("--log", help="Show the log of all version.", action="store_true")
    arg_parser.add_argument("-u", "--update", help="Update cip.", action="store_true")
    arg_parser.add_argument("-v", help="Check the verison of cip.", action="store_true")
    arg_parser.add_argument("--version", help="Check the version of cip with more details.", action="store_true")

    # Parse the arguments
    # 解析参数
    args = arg_parser.parse_args()
    if (args.input or args.file):
        # _DEBUG_FLAG
        # print("参数详情: {:}".format(args))
        tip_msg = "{:} SERVER: {:}:{:}".format("="*5, server_es, server_port)
        print(tip_msg)

        # Use the input "-d" as DNS server
        # 使用输入时指定的dns服务器
        if args.dns:
            # Use input as DNS when
            # 当DNS服务器不为空时, 使用传入的DNS服务器
            server_dns = args.dns
            tip_dns = server_dns
        else:
            tip_dns = "Local DNS"
        tip_dns_msg = "DNS: {:}".format(tip_dns)
        tip_msg = "{:} {:}".format("="*5, tip_dns_msg)
        print(tip_msg)

        if args.input:
            # Use input directly when "-i" exist
            # 存在 -i 时, 将 输入内容 作为输入调用 cip_direct 进行直接输出
            cip_direct(inputs=args.input)
        elif args.file:
            # User file content as input when "-f" exist
            # 存在 -f 时, 将 文件列表 作为输入调用 cip_file 读取并写入文件
            cip_file(files=args.file)
        else:
            print("Input invalidate, we need -i or -f at least")

        # # Show the msg when done
        # 显示运行结束提示
    elif (args.l or args.log):
        # Show the log when "-l" or "--log" are included in arguments
        print(get_log_update(args))
    elif args.update:
        # Update cip when "-u" or "--update"
        update()
    elif (args.v or args.version):
        # Show the version information when "-v" or "--version" inlucde in arguments
        print(get_version(args))
    else:
        # Show help when no arguments illegal
        arg_parser.print_help()
