# encoding=utf-8

"""
dig with multiple DNS
通过多个 DNS 进行解析
"""

import argparse
import csv
import json
from pathlib import Path

from dns import resolver

# Initial path of root, filename and path of input
path_folder = Path(__file__).parent
path_root = path_folder.parent
path_conf_folder = path_root.joinpath("conf")
filename_dns = "dns.json"
path_dns_input = path_conf_folder.joinpath(filename_dns)
path_input_folder = path_conf_folder
filename_hostnames_input = "input_hostnames.txt"
path_hostnames_input = path_input_folder.joinpath(filename_hostnames_input)
var_show_processing = False
var_delimiter_character = ","


def get_dns():
    # Initial a dict of result and read config
    dns_dict = dict()
    with open(file=path_dns_input, mode="r", encoding="utf-8", errors="ignore") as dns_file_obj:
        dns_json = dns_file_obj.read()
        dns_dict = json.loads(dns_json)

    return dns_dict


def get_hostnames():

    hostnames_list = list()

    # Open input file, read the hostnames to list
    with open(file=path_hostnames_input, mode="r", encoding="utf-8", errors="ignore") as obj_hostnames_input:
        hostnames_list = obj_hostnames_input.readlines()
        # Remove the \n of line
        index_tmp = 0
        for index_tmp in range(len(hostnames_list)):
            hostname_tmp = hostnames_list[index_tmp].replace("\n", "")
            hostnames_list[index_tmp] = hostname_tmp

    return hostnames_list


def process_input_std(hostnames, dns_type="A"):
    # Resolve the hostnames
    output_result_hostnames = dict()

    for hostname in hostnames:
        output_result_hostnames[hostname] = resolve_hostname(hostname=hostname, dns_type=dns_type)

    return output_result_hostnames


def process_input_files(files, dns_type="A"):
    output_result_files = "Result of files: {:}".format(files)

    return output_result_files


def resolve_hostname(hostname, dns_type):
    try:
        # Get DNS dict
        dns_dict = get_dns()
        output_result_hostname = dict()
        dns_resolver = resolver.Resolver()
        for dns_server in dns_dict.keys():
            if var_show_processing:
                print_msg = "Working on hostname: {:} of DNS: {:}, ".format(hostname, dns_server)
                print(print_msg, end="")
            output_result_hostname[dns_server] = dns_dict[dns_server]
            dns_resolver.nameservers = [dns_server]
            try:
                dns_response = dns_resolver.resolve(qname=hostname, rdtype=dns_type, lifetime=1)
                if dns_response.rrset:
                    dns_resolve_result = dns_response.rrset.to_text().split()[-1]
            except Exception as expt:
                dns_resolve_result = "Exception: {:}".format(str(expt))
            output_result_hostname[dns_server]["Result"] = dns_resolve_result
            if var_show_processing:
                print_msg = "result: {:}".format(dns_resolve_result)
                print(print_msg)
    except Exception as expt:
        output_result_hostname = {
            "Exception": "{:}, {:}".format(hostname, expt),
        }

    return output_result_hostname


def resolve_hostname_by_dns(hostname, dns):
    resolve_hostname_result = dict()

    return resolve_hostname_result


def output_hostname(hostname):
    # def output_hostname(hostname, output):

    # path_output_folder = path_conf_folder
    # filename_hostnames_output_csv = "output_{:}.csv".format(hostname)
    # path_hostnames_output_csv = path_output_folder.joinpath(filename_hostnames_output_csv)
    # filename_hostnames_output_txt = "output_{:}.txt".format(hostname)
    # path_hostnames_output_txt = path_output_folder.joinpath(filename_hostnames_output_txt)

    # try:
    #     output_result = "finished"
    # except Exception as exception_t:
    #     output_result = str(exception_t)

    output_result = "Output to STR output: {:}".format(hostname)

    return output_result


def output_hostname_csv(hostname):
    # def output_hostname_csv(hostname, output):
    # path_output_folder = path_input_folder
    # filename_hostnames_output = "{:}_output.csv"
    # csv_header = [
    #     "DNS",
    #     "Location",
    #     "Provider",
    #     "Result",
    # ]
    # csv_writer = csv.DictWriter(fieldnames=csv_header, delimiter="|", quotechar="\"")
    # for key_tmp in output.keys():
    #     csv_writer.writerow(
    #         {
    #             csv_header[0]: output[key_tmp],
    #         }
    #     )
    output_result = "Output as CSV: {:}".format(hostname)

    # return
    return output_result


def output_hostname_txt(hostname):
    # def output_hostname_txt(hostname, output):

    output_result = "Output as TXT: {:}".format(hostname)

    return output_result


def output_hostname_txt_deduplicate(output_result):

    print("Deduplicate values in txt.")

    return output_result


def output_hostname_json(hostname):
    # def output_hostname_json(hostname, output):

    output_result = "Output as JSON: {:}".format(hostname)

    return output_result


def process_output(output_result, output_formats, output_deduplicated=False, output_exception=True):
    """
    output result like:
    {
        "csv": {
            "www.akamai.com": [
                "DNS: 1.1.1.1, Location: US, Provider: CloudFlare.com, Result: 23.23.23.23",
                "DNS: 1.1.1.2, Location: US, Provider: CloudFlare.com, Result: 23.23.23.24"
            ],
            "www.akamai.cn": [
                "DNS: 1.1.1.1, Location: US, Provider: CloudFlare.com, Result: 182.91.91.91",
                "DNS: 1.1.1.2, Location: US, Provider: CloudFlare.com, Result: 182.91.91.92"
            ]
        },
        "txt": {
            "www.akamai.com": "23.23.23.23, 23.23.23.24",
            "www.akamai.cn": "182.91.91.91, 182.91.91.92"
        },
        "json": {
            "www.akamai.com": {
                "1.1.1.1": {
                    "DNS": "1.1.1.1",
                    "Location": "US",
                    "Provider": "CloudFlare.com",
                    "Result": "23.23.23.23"
                },
                "1.1.1.2": {
                    "DNS": "1.1.1.2",
                    "Location": "US",
                    "Provider": "CloudFlare.com",
                    "Result": "23.23.23.24"
                }
            },
            "www.akamai.cn": {
                "1.1.1.1": {
                    "DNS": "1.1.1.1",
                    "Location": "US",
                    "Provider": "CloudFlare.com",
                    "Result": "182.91.91.91"
                },
                "1.1.1.2": {
                    "DNS": "1.1.1.2",
                    "Location": "US",
                    "Provider": "CloudFlare.com",
                    "Result": "182.91.91.92"
                }
            }
        }
    }
    """
    output_result_dict = dict()

    # Output with format
    if "csv" in output_formats:
        # Initial the format with csv
        output_result_dict["csv"] = output_result
    if "txt" in output_formats:
        output_result_txt = dict()
        for hostname in output_result.keys():
            output_list_txt = list()
            output_result_txt[hostname] = str()
            for dns_server in output_result[hostname].keys():
                output_dict_txt = output_result[hostname][dns_server]
                if ((output_dict_txt["Result"].startswith("Exception")) and (not output_exception)):
                    continue
                if ((output_dict_txt["Result"] in output_list_txt) and output_deduplicated):
                    continue
                else:
                    output_result_txt[hostname] = "{:}{:}{:}".format(output_result_txt[hostname], output_dict_txt["Result"], var_delimiter_character)
                    output_list_txt.append(output_dict_txt["Result"])
                # Ignore Exception in result: txt
                # output_result_txt[hostname] = output_hostname_content_txt
            if output_result_txt[hostname] == "":
                output_result_txt[hostname] = "{:}".format("NXDOMAIN")
        output_result_dict["txt"] = output_result_txt
    if "json" in output_formats:
        output_result_json = output_result
        output_result_dict["json"] = output_result_json

    return output_result_dict


def process_output_std(output_result, output_formats, output_deduplicate=False, output_exception=False):

    if output_formats == "none":
        pass
    else:
        output_result = process_output(output_result, output_formats=output_formats, output_deduplicated=output_deduplicate, output_exception=output_exception)
        if "csv" in output_formats:
            output_result_csv = dict()
            for hostname in output_result["csv"].keys():
                output_result_csv[hostname] = list()
                for output_key in output_result["csv"][hostname].keys():
                    output_dict_t = output_result["csv"][hostname][output_key]
                    output_hostname_content_csv = "DNS: {:}, Location: {:}, Provider: {:}, Result: {:}".format(
                        output_key, output_dict_t["Location"], output_dict_t["Provider"], output_dict_t["Result"])
                    output_result_csv[hostname].append(output_hostname_content_csv)
            output_result["csv"] = output_result_csv
        output_result_json = json.dumps(output_result, ensure_ascii=False, indent=4)
        print_msg = """
        ====> Result:
        {:}
        """.format(output_result_json)
        print(print_msg)


def process_output_file(output_result, output_formats, output_deduplicate=False):

    save_result = output_formats

    return save_result


def load_version():
    path_file_version = path_folder.joinpath("version")
    with open(file=path_file_version, mode="r", encoding="utf-8", errors="ignore") as file_obj_version:
        file_content_version = file_obj_version.read()
        info_version = file_content_version
        return info_version


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog="akdig", description="Resolve the hostnames with multiple DNS.")
    arg_parser.add_argument("-i", "--inputs", type=str, nargs="+", help="Use hostnames as input, split with white space.")
    arg_parser.add_argument("-f", "--files", type=str, nargs="+", help="(Unsupported now)\nUse files as input, split with white space.")
    arg_parser.add_argument("-o", "--output", type=str, nargs="+", default="none", help="Output with [json|csv|txt] format. Can be multiple values. Default: json.")
    arg_parser.add_argument("-c", "--character", type=str, default=",", help="Character of delimiter with output format: txt. Default: \",\".")
    arg_parser.add_argument("-t", "--type", action="store", default="A", help="Resolve the specific record type. Default: A.")
    arg_parser.add_argument("-s", "--save", action="store_true", help="(Unsupported now)\nSave output with specific format as file with filename same as hostnames.")
    arg_parser.add_argument("-d", "--deduplicate", action="store_true", help="Remove the duplicated values in result with txt format.")
    arg_parser.add_argument("-p", "--processing", action="store_false", help="Don't display the processing.")
    arg_parser.add_argument("-e", "--exception", action="store_true", help="Include exception in result with txt format.")
    arg_parser.add_argument("-v", "--version", action="version", version=load_version())
    args = arg_parser.parse_args()
    # __DEBUG_FLAG__: inputs
    # args = arg_parser.parse_args("-i www.akamai.com -o txt".split())

    # Set output_delimiter
    var_delimiter_character = args.character

    # Get all the hostnames
    if args.processing:
        var_show_processing = args.processing

    if (args.inputs or args.files):
        if args.inputs:
            output_result = process_input_std(hostnames=args.inputs, dns_type=args.type)
        elif args.files:
            output_result = process_input_files(files=args.files, dns_type=args.type)

        # Save to file or not
        if args.save:
            # Save to file if true
            process_result = process_output_file(output_result=output_result, output_formats=args.output, output_deduplicate=args.deduplicate, output_exception=args.exception)
            process_result_json = json.dumps(process_result, ensure_ascii=False, indent=4)
            print(process_result_json)
        else:
            # Or use standard output
            process_output_std(output_result=output_result, output_formats=args.output, output_deduplicate=args.deduplicate, output_exception=args.exception)
