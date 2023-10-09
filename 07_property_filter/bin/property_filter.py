#!/usr/bin/python3
# encoding=utf-8


import csv
import json
import sys
from pathlib import Path

import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc

# Args: [edgercSection, accountSwitchKey, filterName]
# sys.argv = [Path(__file__), "aaa", "ctrip", "cm"]
edgerc_section = sys.argv[1]
edgerc_section_ask = sys.argv[2]
filter_name = sys.argv[3]
if filter_name == "aic":
    filter_conditions = "$..behaviors[?(@.name == 'adaptiveImageCompression')]"
    filter_name_full = "AdaptiveImageCompression"
if filter_name == "cm":
    filter_conditions = "$..behaviors[?(@.name == 'edgeConnect')]"
    filter_name_full = "CloudMonitor"

# filter_conditions = "$..behaviors[?(@.name == 'origin')]"
# filter_conditions = "$..behaviors[?(@.name == 'origin' && @.options.hostname == 'ak-origin.aojie654.com')]"

result_dir = Path(__file__).parents[1].joinpath("output")
result_filename_json = "{:}_{:}.json".format(edgerc_section_ask, filter_name_full)
result_path_json = result_dir.joinpath(result_filename_json)
result_filename_csv = "{:}_{:}.csv".format(edgerc_section_ask, filter_name_full)
result_path_csv = result_dir.joinpath(result_filename_csv)

if not result_dir.exists():
    result_dir.mkdir()

print_msg = {
    "EdgeRC Section": edgerc_section,
    "Account": edgerc_section_ask,
    "Filter Name": filter_name_full,
    "Filter Conditions": filter_conditions,

}
print_msg = json.dumps(print_msg, ensure_ascii=False, indent=4)
print(print_msg)

# Akamai Beijing: sao
contract_id = ""
group_id = ""


edgerc_path = Path("~/.edgerc")
edgerc_obj = EdgeRc(filename=edgerc_path)
if edgerc_section_ask != "":
    api_ask = edgerc_obj.get(edgerc_section_ask, "account_switch_key")
else:
    api_ask = ""
api_host = edgerc_obj.get(section=edgerc_section, option="host")
api_uri = "/papi/v1/bulk/rules-search-requests-synch"

req_url = "https://{:}{:}".format(api_host, api_uri)

req_method = "POST"

req_params = {}
if api_ask != "":
    req_params["accountSwitchKey"] = api_ask
if contract_id != "":
    req_params["contractId"] = contract_id
if group_id != "":
    req_params["groupId"] = group_id

req_headers = {
    "accept": "application/json",
    "PAPI-Use-Prefixes": "true",
    "content-type": "application/json"
}

req_payload = {
    "bulkSearchQuery":
    {
        # "bulkSearchQualifiers": ["$.options[?(@.secure==\"true\")]", "$..features[?(@.name==\"origin\")].options[?(@.hostname==\"old.origin.example.com\")]"],
        "match": filter_conditions,
        "syntax": "JSONPATH",
    }
}

req_session = requests.Session()
req_session.auth = EdgeGridAuth.from_edgerc(edgerc_obj, edgerc_section)
req_result = req_session.request(method=req_method, url=req_url, params=req_params, headers=req_headers, json=req_payload)
rep_dict = req_result.json()

if req_result.status_code != 200:
    # print_msg = json.dumps(rep_dict, ensure_ascii=False)
    print_msg = json.dumps(rep_dict, ensure_ascii=False, indent=4)
    print(print_msg)
else:
    # Original results in json
    result_dict = rep_dict["results"]

    # Save to json file
    with open(file=result_path_json, mode="w+", encoding="utf-8", errors="ignore") as result_file_json:
        result_dict_jsoned = json.dumps(result_dict, ensure_ascii=False, indent=4)
        result_file_json.write(result_dict_jsoned)
        print_msg = "Result: JSON saved to {:}".format(result_path_json)
        print(print_msg)
        result_file_json.close()

    # Formated results
    result_dict = dict()
    result_csv_headers = ["property", "staging version", "staging status", "staging rule locations", "production version", "production status",  "production rule locations"]
    prop_list = rep_dict["results"]
    if len(prop_list) > 0:
        for prop_tmp in prop_list:
            prop_tmp_name = prop_tmp["propertyName"]
            if prop_tmp_name not in result_dict.keys():
                result_dict[prop_tmp_name] = {
                    result_csv_headers[0]: prop_tmp["propertyName"],
                    result_csv_headers[1]: "N/A",
                    result_csv_headers[2]: "N/A",
                    result_csv_headers[3]: "N/A",
                    result_csv_headers[4]: "N/A",
                    result_csv_headers[5]: "N/A",
                    result_csv_headers[6]: "N/A",
                }
            else:
                pass
            if prop_tmp["stagingStatus"] == "ACTIVE":
                # if result_dict[prop_tmp_name][result_csv_headers[1]] == "N/A":
                result_dict[prop_tmp_name][result_csv_headers[1]] = prop_tmp["propertyVersion"],
                result_dict[prop_tmp_name][result_csv_headers[2]] = prop_tmp["stagingStatus"],
                result_dict[prop_tmp_name][result_csv_headers[3]] = prop_tmp["matchLocations"],
                # print(type(prop_tmp["propertyVersion"]), type(result_dict[prop_tmp_name][result_csv_headers[1]]))
            else:
                pass
            if prop_tmp["productionStatus"] == "ACTIVE":
                # if result_dict[prop_tmp_name][result_csv_headers[4]] == "N/A":
                result_dict[prop_tmp_name][result_csv_headers[4]] = prop_tmp["propertyVersion"],
                result_dict[prop_tmp_name][result_csv_headers[5]] = prop_tmp["productionStatus"],
                result_dict[prop_tmp_name][result_csv_headers[6]] = prop_tmp["matchLocations"],
                # print(type(prop_tmp["propertyVersion"]), type(result_dict[prop_tmp_name][result_csv_headers[4]]))
            else:
                pass
    with open(file=result_path_csv, mode="w+", encoding="utf-8", errors="ignore") as result_file_csv:
        csv_writer = csv.DictWriter(result_file_csv, fieldnames=result_csv_headers)
        csv_writer.writeheader()
        for result_item in result_dict.values():
            csv_writer.writerow(result_item)
        print_msg = "Result: CSV saved to {:}".format(result_path_json)
        print(print_msg)
