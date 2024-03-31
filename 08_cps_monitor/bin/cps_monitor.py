# encoding=utf-8
import argparse
import csv
import json
import logging
import sys
from datetime import datetime
from logging import Logger
from pathlib import Path

from akamai.edgegrid import EdgeGridAuth, EdgeRc
from requests import Session


def path_init():
    # Initial paths
    path_file = Path(__file__)
    path_bin = path_file.parent
    path_home = path_bin.parent

    return path_home


def date_init():
    date_dt = datetime.now()
    date_str = datetime.strftime(date_dt, "%Y%m%d")

    return date_str


def log_init():
    # Log path
    name_folder_log = "log"
    path_home = path_init()
    path_folder_log = path_home.joinpath(name_folder_log)
    if not path_folder_log.exists:
        log_msg = "Log folder:{:} not exist, create one.".format(path_folder_log)
        print(log_msg)
        path_folder_log.mkdir()
    else:
        pass
    date_str = date_init()
    name_file_log = "cps_monitor_{:}.log".format(date_str)
    path_file_log = path_folder_log.joinpath(name_file_log)
    log_msg = "Log Path is: {:}".format(path_file_log)
    logger = logging.getLogger(__file__)
    logging.basicConfig(filename=path_file_log, encoding='utf-8', level=logging.INFO, format='%(asctime)s; %(levelname)s; %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    print(log_msg)
    logger.info(log_msg)

    return logger


def config_processor(logger: Logger, config_action: str, config_obj: dict = dict()):
    # Config path
    name_folder_conf = "conf"
    path_home = path_init()
    path_folder_conf = path_home.joinpath(name_folder_conf)
    name_file_conf = "conf.json"
    path_file_conf = path_folder_conf.joinpath(name_file_conf)
    if config_action == "load":
        if (not path_file_conf.exists):
            log_msg = "Conf: {:} not exist, exit.".format(path_file_conf)
            print(log_msg)
            logger.error(log_msg)
            exit()

        with open(file=path_file_conf, mode="r", encoding="utf-8", errors="ignore") as conf_file_obj:
            conf_file_str = conf_file_obj.read()
            conf_file_json = json.loads(conf_file_str)
            conf_file_obj.close()

        log_msg = "Config loaded."
        print(log_msg)
        logger.info(log_msg)

        return conf_file_json
    elif config_action == "save":
        with open(file=path_file_conf, mode="w+", encoding="utf-8", errors="ignore") as conf_file_obj:
            config_jsonfy = json.dumps(config_obj, ensure_ascii=False, indent=4)
            conf_file_obj.write(config_jsonfy)
            conf_file_obj.close()
        log_msg = "Config saved."
        print(log_msg)
        logger.info(log_msg)


def edgerc_init(logger: Logger, config_obj: dict):
    path_home = Path().home()
    path_file_edgerc = path_home.joinpath(".edgerc")
    edgerc_section = config_obj["api_client"]["section"]
    edgerc_obj = EdgeRc(path_file_edgerc)
    api_host = edgerc_obj.get(section=edgerc_section, option="host")
    log_msg = "Config: {:} loaded, Api client section: {:}.".format(path_file_edgerc, edgerc_section)
    print(log_msg)
    logger.info(log_msg)

    return edgerc_obj, edgerc_section, api_host


def accounts_processor(logger: Logger, config_obj: dict, command_type: str, accounts_list: list):
    if command_type not in ["add", "remove"]:
        log_msg = "Invalid command: {:}.".format(command_type)
    else:
        if command_type == "add":
            for account in accounts_list:
                config_obj = account_add(logger=logger, config_obj=config_obj, account=account)
        elif command_type == "remove":
            for account in accounts_list:
                config_obj = account_remove(logger=logger, config_obj=config_obj, account=account)

        config_processor(logger=logger, config_action="save", config_obj=config_obj)
        log_msg = "Accounts: {:} processed.".format(accounts_list)

    return log_msg


def account_add(logger: Logger, config_obj: dict, account: str):
    log_msg = str()
    account_ask, account_name = account.split("|")
    if account_ask in config_obj["accounts"].keys():
        log_msg = "Account: {:}|{:} already exist in account list.".format(account_ask, account_name)
    else:
        config_obj["accounts"][account_ask] = account_name
        log_msg = "Account: {:}|{:} added.".format(account_ask, account_name)
    print(log_msg)
    logger.info(log_msg)

    return config_obj


def account_remove(logger: Logger, config_obj: dict, account: str):
    log_msg = str()
    account_ask = account
    account_name = config_obj["accounts"][account_ask]
    if account_ask not in config_obj["accounts"].keys():
        log_msg = "Account: {:}|{:} not in account list.".format(account_ask, account_name)
    else:
        config_obj["accounts"].pop(account_ask)
        log_msg = "Account: {:}|{:} removed.".format(account_ask, account_name)

    print(log_msg)
    logger.info(log_msg)

    return config_obj


def users_processor(logger: Logger, config_obj: dict, command_type: str, user_list: list, account_asks: list):
    if command_type == "add":
        for account_ask in account_asks:
            for user_id in user_list:
                user_add(logger=logger, config_obj=config_obj, user_id=user_id, account_ask=account_ask)
        log_msg = "Users: {:} added.".format(user_list)
    elif command_type == "remove":
        for account_ask in account_asks:
            for user_id in user_list:
                user_remove(logger=logger, config_obj=config_obj, user_id=user_id, account_ask=account_ask)
        log_msg = "Users: {:} removed.".format(user_list)
    else:
        log_msg = "Invalid command: {:}.".format(command_type)

    return log_msg


def user_get(logger: Logger, config_obj: dict, account_ask: str):
    users_list = list()

    return users_list


def user_add(logger: Logger, config_obj: dict, user_id: str, account_ask: str):
    log_msg = "User: {:} added to account: {:}.".format(user_id, account_ask)

    print(log_msg)
    logger.info(log_msg)

    return config_obj


def user_remove(logger: Logger, config_obj: dict, user_id: str, account_ask: str):
    log_msg = "User: {:} removed from account: {:}.".format(user_id, account_ask)

    print(log_msg)
    logger.info(log_msg)

    return config_obj


def slots_processor(logger: Logger, config_obj: dict):
    req_obj, api_host = request_init(logger=logger, config_obj=config_obj)
    csv_file, csv_path_file, csv_obj, csv_headers = csv_init(logger=logger)
    for account_ask in config_obj["accounts"].keys():
        account_name = config_obj["accounts"][account_ask]
        contract_list = contracts_get(logger=logger, api_host=api_host, req_obj=req_obj, account=account_ask)
        if contract_list[0] == "N/A":
            log_msg = "Errors when get contract list."
            logger.error(log_msg)
        else:
            for contract_id in contract_list:
                slot_list_enrollments(logger=logger, csv_obj=csv_obj, csv_headers=csv_headers, req_obj=req_obj, api_host=api_host, account_ask=account_ask, account_name=account_name, contract_id=contract_id)
            log_msg = "Slots processed."
            logger.info(log_msg)
        print(log_msg)
    csv_file.close()
    log_msg = "Output: CSV: {:}.".format(csv_path_file)
    return log_msg


def slot_list_enrollments(logger: Logger, csv_obj: csv.DictWriter, csv_headers: str, req_obj: Session, api_host: str, account_ask: str, account_name: str, contract_id: str):
    log_msg = str()
    api_method = "GET"
    api_uri = "/cps/v2/enrollments"
    api_url = "https://{:}{:}".format(api_host, api_uri)
    api_headers = {
        "accept": "application/vnd.akamai.cps.enrollments.v11+json",
    }
    contract_id = contract_id.replace("ctr_", "")
    enrollment_obj = {
        csv_headers[0]: account_name,
        csv_headers[1]: account_ask,
        csv_headers[2]: contract_id,
    }
    try:
        api_params = {
            "accountSwitchKey": account_ask,
            "contractId": contract_id,
        }
        rsp_obj = req_obj.request(method=api_method, url=api_url, params=api_params, headers=api_headers)
        if rsp_obj.status_code == 200:
            rsp_obj_json = rsp_obj.json()
            if len(rsp_obj_json["enrollments"]) == 0:
                log_msg = "No enrollments in contract: {:} > {:}".format(account_name, contract_id)
                logger.info(log_msg)
            else:
                for enrollment_item in rsp_obj_json["enrollments"]:
                    if len(enrollment_item["pendingChanges"]) == 0:
                        continue
                    else:
                        for pending_change in enrollment_item["pendingChanges"]:
                            if (("changeType" in pending_change.keys()) and (pending_change["changeType"] == "renewal")):
                                slot_cn = enrollment_item["csr"]["cn"]
                                slot_id = enrollment_item["assignedSlots"][0]
                                enrollment_obj[csv_headers[3]] = slot_cn
                                enrollment_obj[csv_headers[4]] = slot_id
                                csv_obj.writerow(enrollment_obj)
                                log_msg = "Add enrollment: {:}".format(enrollment_obj)
                                logger.info(log_msg)
                            else:
                                enrollment_obj[csv_headers[3]] = "N/A"
                                enrollment_obj[csv_headers[4]] = "N/A"
                                continue
        else:
            log_msg = "{:}: {:}".format(rsp_obj.status_code, rsp_obj.text)
            raise Exception(log_msg)
    except Exception as e:
        log_msg = e
        logger.error(log_msg)
    finally:
        print(log_msg)

    return


def contracts_get(logger: Logger, api_host: str, req_obj: Session, account: str):
    contract_list = list()

    api_method = "GET"
    api_uri = "/papi/v1/contracts"
    api_url = "https://{:}{:}".format(api_host, api_uri)
    api_params = {
        "accountSwitchKey": account,
    }
    api_headers = {
        "PAPI-Use-Prefixes": "true",
        "accept": "application/json",
    }

    try:
        rsp_obj = req_obj.request(method=api_method, url=api_url, params=api_params, headers=api_headers)
        if rsp_obj.status_code == 200:
            rsp_obj_json = rsp_obj.json()
            for item in rsp_obj_json["contracts"]["items"]:
                contract_list.append(item["contractId"])
            config_obj[account] = contract_list
            log_msg = "Add account: {:} with contracts: {:}".format(account, contract_list)
            logger.info(log_msg)
        else:
            log_msg = "{:}: {:}".format(rsp_obj.status_code, rsp_obj.text)
            raise Exception(log_msg)
    except Exception as e:
        log_msg = e.with_traceback()
        print(log_msg)
        logger.error(log_msg)
        contract_list.append("N/A")

    finally:
        print(log_msg)

    return contract_list


def request_init(logger: Logger, config_obj: dict):
    edgerc_obj, edgerc_section, api_host = edgerc_init(logger=logger, config_obj=config_obj)
    req_obj = Session()
    req_obj.auth = EdgeGridAuth.from_edgerc(rcinput=edgerc_obj, section=edgerc_section)

    return req_obj, api_host


def csv_init(logger: Logger):
    date_str = date_init()
    csv_filename = "result_{:}.csv".format(date_str)
    csv_path_folder = path_init().joinpath("output")
    csv_path_file = csv_path_folder.joinpath(csv_filename)
    if (csv_path_folder.exists()):
        log_msg = "CSV path: {:} exist, create skipped.".format(csv_path_folder)
    else:
        log_msg = "CSV path: {:} not exist, create one.".format(csv_path_folder)
        csv_path_folder.mkdir()
    logger.info(log_msg)
    csv_file = open(file=csv_path_file, mode="w+", encoding="utf-8", errors="ignore")
    csv_headers = ["Account Name", "Account Switch Key", "Contract", "Common Name", "Slot ID"]
    csv_obj = csv.DictWriter(f=csv_file, fieldnames=csv_headers)
    csv_obj.writeheader()

    return csv_file, csv_path_file, csv_obj, csv_headers


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Akamai CPS monitor.")
    arg_parser.add_argument("-a", "--accounts", nargs="+", type=str, help="Account switch keys and account name. Format: \"ask|name\". Default: None.")
    arg_parser.add_argument("-u", "--users", nargs="+", type=str, help="User IDs. Default: None.")
    arg_parser.add_argument("-c", "--command", type=str, default="add", help="Values: [add|remove]. Default: add.")
    arg_parser.add_argument("-s", "--slot", action="store_true", help="List enrolling slots. No command required.")

    # __DEBUG_FLAG__
    # sys.argv = [__file__, "-c", "add", "-a", "1-AAAAA|Example.com"]
    # sys.argv = [__file__, "-s"]
    args = arg_parser.parse_args()
    if (args.accounts or args.slot):
        logger = log_init()
        config_obj = config_processor(logger=logger, config_action="load")
        if (args.accounts or args.users):
            if args.accounts:
                if (not args.users):
                    result_processor = accounts_processor(logger=logger, config_obj=config_obj, command_type=args.command, accounts_list=args.accounts, )
                else:
                    result_processor = users_processor(logger=logger, config_obj=config_obj, command_type=args.command, user_list=args.users, account_asks=args.accounts)
            else:
                pass
        elif args.slot:
            result_processor = slots_processor(logger=logger, config_obj=config_obj)
        else:
            pass
        print(result_processor)
        logger.info(result_processor)
    else:
        arg_parser.print_help()