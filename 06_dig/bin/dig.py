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
path_dir_conf = path_root.joinpath("conf")
filename_dns = "dns.json"
path_file_dns_input = path_dir_conf.joinpath(filename_dns)
path_dir_input = path_dir_conf
filename_hostnames_input = "input_hostnames.txt"
path_file_hostnames_input = path_dir_input.joinpath(filename_hostnames_input)
var_show_processing = False
var_delimiter_character = ","


def get_dns():
    # Initial a dict of result and read config
    dns_dict = dict()
    with open(file=path_file_dns_input, mode="r", encoding="utf-8", errors="ignore") as dns_file_obj:
        dns_json = dns_file_obj.read()
        dns_dict = json.loads(dns_json)

    return dns_dict


def get_hostnames():

    hostnames_list = list()

    # Open input file, read the hostnames to list
    with open(file=path_file_hostnames_input, mode="r", encoding="utf-8", errors="ignore") as obj_hostnames_input:
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
        hostname = hostname.lower()
        if hostname in output_result_hostnames.keys():
            continue
        else:
            pass
        output_result_hostnames[hostname] = resolve_hostname(hostname=hostname, dns_type=dns_type)

    return output_result_hostnames


def process_input_files(files, dns_type="A"):
    hostnames = list()
    for file in files:
        with open(file=file, mode="r", encoding="utf-8", errors="ignore") as file_obj:
            file_lines = file_obj.read().splitlines()
            hostnames = hostnames + file_lines
    output_result_files = process_input_std(hostnames=hostnames, dns_type=dns_type)

    return output_result_files


def resolve_hostname(hostname, dns_type):
    try:
        # Get DNS dict
        dns_dict = get_dns()
        output_result_hostname = dict()
        dns_resolver = resolver.Resolver()
        for dns_server in dns_dict.keys():
            hostname_t = hostname
            if var_show_processing:
                print_msg = "Working on hostname: {:} of DNS: {:}, ".format(hostname_t, dns_server)
                print(print_msg, end="")
            output_result_hostname[dns_server] = dns_dict[dns_server]
            dns_resolver.nameservers = [dns_server]
            try:
                dns_resolve_result = str()
                while True:
                    try:
                        dns_response = dns_resolver.resolve(qname=hostname_t, rdtype=dns_type, lifetime=1)
                    except resolver.NoAnswer:
                        break
                    else:
                        dns_resolve_result_t = dns_response.rrset.to_text().split()[-1]
                        dns_resolve_result = "{:} : {:}".format(dns_resolve_result, dns_resolve_result_t)
                        if (dns_type.upper() != "CNAME"):
                            break
                        else:
                            hostname_t = dns_resolve_result_t
                dns_resolve_result = dns_resolve_result[3:]
            except resolver.LifetimeTimeout:
                dns_resolve_result = "Exception: DNS timeout"
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
    if "json" in output_formats:
        output_result_json = output_result
        output_result_dict["json"] = output_result_json
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

    return


def process_output_file(output_result, record_type, filename_output, output_formats,  output_deduplicate=False, output_exception=False):
    output_result = process_output(output_result, output_formats=output_formats, output_deduplicated=output_deduplicate, output_exception=output_exception)

    path_dir_output = path_root.joinpath("output")
    if Path.exists(path_dir_output):
        pass
    else:
        Path.mkdir(path_dir_output)

    if filename_output.lower() == "h":
        process_output_file_hostnames(output_result=output_result, record_type=record_type, path_dir_output=path_dir_output, output_formats=output_formats)
    else:
        process_output_file_single(output_result=output_result, record_type=record_type, filename_output=filename_output,
                                   path_dir_output=path_dir_output, output_formats=output_formats)

    return


def process_output_file_hostnames(output_result, record_type, path_dir_output, output_formats):
    # Search each format
    for output_format in output_formats:
        output_result_format = output_result[output_format]
        # Search each hostname
        for hostname_tmp in output_result_format.keys():
            # Generate the filename and path
            filename_output_result = "{:}_{:}.{:}".format(hostname_tmp, record_type, output_format)
            path_file_hostname_output = path_dir_output.joinpath(filename_output_result)
            with open(file=path_file_hostname_output, mode="w+", encoding="utf-8", errors="ignore") as output_file_obj:
                # Get the result of hostname
                output_result_format_hostname = output_result_format[hostname_tmp]
                # Save the file by format
                if output_format == "json":
                    # Save text with jsoned format
                    output_result_format_result = json.dumps(output_result_format_hostname, ensure_ascii=False, indent=4)
                    output_file_obj.write(output_result_format_result)
                elif output_format == "csv":
                    # Generate headers and write
                    csv_headers = ["DNS", "Location", "Provider", "Type",  "Result"]
                    csv_writer = csv.DictWriter(output_file_obj, csv_headers)
                    csv_writer.writeheader()
                    # Insert the type to result and write
                    for csv_item in output_result_format_hostname.values():
                        csv_item["Type"] = record_type
                        csv_writer.writerow(csv_item)
                elif output_format == "txt":
                    # Save the text directly
                    output_result_format_result = output_result_format_hostname
                    output_file_obj.write(output_result_format_result)
            # Close the file reated to hostname in the loop of hostname
            print_msg = "OUTPUT: {:} with record type: {:} is saved to {:}".format(hostname_tmp, record_type, path_file_hostname_output)
            print(print_msg)

    return


def process_output_file_single(output_result, record_type, filename_output, path_dir_output, output_formats):
    # Search each format
    for output_format in output_formats:
        output_result_format = output_result[output_format]
        # Open the result file out of the loop of hostnames
        filename_output_result = "{:}_{:}.{:}".format(filename_output, record_type, output_format)
        path_file_hostname_output = path_dir_output.joinpath(filename_output_result)
        output_file_obj = open(file=path_file_hostname_output, mode="w+", encoding="utf-8", errors="ignore")
        # Search each hostname
        # Save the file by format
        if output_format == "json":
            # Add hostname for the values
            output_result_format = json.dumps(output_result_format, ensure_ascii=False, indent=4)
            output_file_obj.write(output_result_format)
        elif output_format == "csv":
            csv_headers = ["Hostname", "DNS", "Location", "Provider", "Type",  "Result"]
            csv_writer = csv.DictWriter(output_file_obj, csv_headers)
            csv_writer.writeheader()
            for hostname_tmp in output_result_format.keys():
                output_result_format_hostname = output_result_format[hostname_tmp]
                for csv_item in output_result_format_hostname.values():
                    csv_item[csv_headers[0]] = hostname_tmp
                    csv_item["Type"] = record_type
                    csv_writer.writerow(csv_item)
        elif output_format == "txt":
            for hostname_tmp in output_result_format.keys():
                output_result_format_hostname = "{:}: {:}\n".format(hostname_tmp, output_result_format[hostname_tmp])
                output_file_obj.write(output_result_format_hostname)
        # Close the file out of the loop of hostname
        output_file_obj.close()
        print_msg = "OUTPUT: {:} with record type: {:} is saved to {:}".format(hostname_tmp, record_type, path_file_hostname_output)
        print(print_msg)

    return


def load_version():
    path_file_version = path_folder.joinpath("version")
    with open(file=path_file_version, mode="r", encoding="utf-8", errors="ignore") as file_obj_version:
        file_content_version = file_obj_version.read()
        info_version = file_content_version
        return info_version


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog="akdig", description="Resolve the hostnames with multiple DNS.")
    arg_parser.add_argument("-c", "--character", type=str, default=",", help="Character of delimiter with output format: txt. Default: \",\".")
    arg_parser.add_argument("-d", "--deduplicate", action="store_true", help="Remove the duplicated values in result with txt format.")
    arg_parser.add_argument("-e", "--exception", action="store_true", help="Include exception in result with txt format.")
    arg_parser.add_argument("-f", "--files", type=str, nargs="+", help="Use files as input, split with white space.")
    arg_parser.add_argument("-i", "--inputs", type=str, nargs="+", help="Use hostnames as input, split with white space.")
    arg_parser.add_argument("-o", "--output", type=str, nargs="+", default="none", help="Output with [json|csv|txt] format. Can be multiple values. Default: json.")
    arg_parser.add_argument("-p", "--processing", action="store_false", help="Don't display the processing.")
    arg_parser.add_argument("-s", "--save", action="store", default=False, help="Save output with specific format as file, 'h' to same as hostname, and other to filename.")
    arg_parser.add_argument("-t", "--type", action="store", default="A", help="Resolve the specific record type. Default: A.")
    arg_parser.add_argument("-v", "--version", action="version", version=load_version())
    args = arg_parser.parse_args()
    # __DEBUG_FLAG__: inputs
    # args_str = "-i www.ctrip.com -t CNAME -o csv"
    # args_str = "-i www.ctrip.com -t CNAME -o txt -d"
    # args_str = "-i www.aojie654.com www.akasao.com -t CNAME -o txt csv json -d -s h"
    # args = arg_parser.parse_args(args_str.split())

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
            process_output_file(output_result=output_result, record_type=args.type, filename_output=args.save,
                                output_formats=args.output, output_deduplicate=args.deduplicate, output_exception=args.exception)
        else:
            # Or use standard output
            process_output_std(output_result=output_result, output_formats=args.output, output_deduplicate=args.deduplicate, output_exception=args.exception)
