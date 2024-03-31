#!/usr/bin/python3
# encoding=utf-8


import csv
import jsonc
import sys
from pathlib import Path
from datetime import datetime

import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc

# __DEBUG_FLAG__: Args: [edgercSection, accountSwitchKey, filterName]
# sys.argv = [Path(__file__), "aaa", "ctrip", "aic"]

# Generate the vars
edgerc_section = sys.argv[1]
edgerc_section_ask = sys.argv[2]
path_root = Path(__file__).parents[1]
path_conf = path_root.joinpath("conf")
path_conf_behaviors = path_conf.joinpath("behaviors.json")
filter_name_full = str()
filter_conditions = str()

# Read the name and match from json
try:
    with open(path_conf_behaviors, mode="r", encoding="utf-8", errors="ignore") as obj_json_behaviors:
        content_behaviors = obj_json_behaviors.read()
        content_behaviors_json = jsonc.loads(content_behaviors)
        filter_name_short = sys.argv[3]
        filter_name_full = content_behaviors_json[filter_name_short]["name_full"]
        filter_conditions = content_behaviors_json[filter_name_short]["match"]

except Exception as tmp_exception:
    print(tmp_exception.with_traceback())
    exit()

# filter_conditions = "$..behaviors[?(@.name == 'origin')]"
# filter_conditions = "$..behaviors[?(@.name == 'origin' && @.options.hostname == 'ak-origin.aojie654.com')]"

# Generate Filename
result_ts = datetime.now()
result_ts_file = datetime.strftime(result_ts, "%Y%m%d-%H%M%S")
result_dir = Path(__file__).parents[1].joinpath("output")
result_file_name = "{:}_{:}_{:}".format(result_ts_file, edgerc_section_ask, filter_name_full)
result_file_path = result_dir.joinpath(result_file_name)
result_path_json = result_file_path.with_suffix(".json")
result_path_csv = result_file_path.with_suffix(".csv")

# Create folder if not exist
if not result_dir.exists():
    result_dir.mkdir()

# Generate the print message
print_msg = {
    "EdgeRC Section": edgerc_section,
    "Account": edgerc_section_ask,
    "Filter Name": filter_name_full,
    "Filter Conditions": filter_conditions,

}
print_msg = jsonc.dumps(print_msg, ensure_ascii=False, indent=4)
print(print_msg)

# Initial vars
contract_id = ""
group_id = ""

# Initial edgerc
edgerc_path = Path("~/.edgerc")
edgerc_obj = EdgeRc(filename=edgerc_path)
if edgerc_section_ask != "":
    api_ask = edgerc_obj.get(edgerc_section_ask, "account_switch_key")
else:
    api_ask = ""

# Initial API Info
api_host = edgerc_obj.get(section=edgerc_section, option="host")
api_uri = "/papi/v1/bulk/rules-search-requests-synch"
req_url = "https://{:}{:}".format(api_host, api_uri)
req_method = "POST"

# Initial authorization info
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

# Bulk search
req_payload = {
    "bulkSearchQuery":
    {
        # "bulkSearchQualifiers": ["$.options[?(@.secure==\"true\")]", "$..features[?(@.name==\"origin\")].options[?(@.hostname==\"old.origin.example.com\")]"],
        "match": filter_conditions,
        "syntax": "JSONPATH",
    }
}

# Create reuqest session
req_session = requests.Session()
req_session.auth = EdgeGridAuth.from_edgerc(edgerc_obj, edgerc_section)
req_result = req_session.request(method=req_method, url=req_url, params=req_params, headers=req_headers, json=req_payload)
rep_dict = req_result.json()

# Match the response
if req_result.status_code != 200:
    # print_msg = jsonc.dumps(rep_dict, ensure_ascii=False)
    print_msg = jsonc.dumps(rep_dict, ensure_ascii=False, indent=4)
    print(print_msg)
else:
    # Original results in json
    result_dict = rep_dict["results"]

    # Save to json file
    with open(file=result_path_json, mode="w+", encoding="utf-8", errors="ignore") as result_file_json:
        result_dict_jsoned = jsonc.dumps(result_dict, ensure_ascii=False, indent=4)
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
                result_dict[prop_tmp_name][result_csv_headers[1]] = prop_tmp["propertyVersion"]
                result_dict[prop_tmp_name][result_csv_headers[2]] = prop_tmp["stagingStatus"]
                result_dict[prop_tmp_name][result_csv_headers[3]] = prop_tmp["matchLocations"]
                # print(type(prop_tmp["propertyVersion"]), type(result_dict[prop_tmp_name][result_csv_headers[1]]))
            else:
                pass
            if prop_tmp["productionStatus"] == "ACTIVE":
                # if result_dict[prop_tmp_name][result_csv_headers[4]] == "N/A":
                result_dict[prop_tmp_name][result_csv_headers[4]] = prop_tmp["propertyVersion"]
                result_dict[prop_tmp_name][result_csv_headers[5]] = prop_tmp["productionStatus"]
                result_dict[prop_tmp_name][result_csv_headers[6]] = prop_tmp["matchLocations"]
                # print(type(prop_tmp["propertyVersion"]), type(result_dict[prop_tmp_name][result_csv_headers[4]]))
            else:
                pass

    # Write to file
    with open(file=result_path_csv, mode="w+", encoding="utf-8", errors="ignore") as result_file_csv:
        csv_writer = csv.DictWriter(result_file_csv, fieldnames=result_csv_headers)
        csv_writer.writeheader()
        for result_item in result_dict.values():
            csv_writer.writerow(result_item)
        print_msg = "Result: CSV saved to {:}".format(result_path_csv)
        print(print_msg)
