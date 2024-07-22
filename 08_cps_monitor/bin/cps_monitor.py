# encoding=utf-8
import argparse
import json
import logging
import time
from datetime import datetime, timezone
from logging import Logger
from pathlib import Path
import re

import pandas
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from requests import Session


def add_accounts(logger: Logger, conf_obj: dict, account: str):
    account_ask, account_name = account.split("^")
    if account_ask in conf_obj["accounts"].keys():
        log_msg = "{:}; Account already exist: {:}|{:}".format(add_accounts.__name__, account_ask, account_name)
    else:
        conf_obj["accounts"][account_ask] = {
            "name": account_name,
            "users": list(),
        }
        log_msg = "{:}; Account added: {:}|{:}".format(add_accounts.__name__, account_ask, account_name)
    print(log_msg)
    logger.info(log_msg)

    return conf_obj


def add_user(logger: Logger, conf_obj: dict, user_set: set, account: str):
    if ("^" in account):
        # Create account if no such account
        account_ask, account_name = account.split("^")
    else:
        account_ask = account
    if (account_ask not in conf_obj["accounts"].keys()):
        conf_obj["accounts"][account_ask] = {
            "name": account_name,
            "users": list()
        }
        log_msg = "{:}; No such account: {:}, create one.".format(add_user.__name__, account)
    else:
        log_msg = "{:}; Found account: {:}, create skipped.".format(add_user.__name__, account)
    print(log_msg)
    user_list_account = conf_obj["accounts"][account_ask]["users"]
    log_msg = "{:}; Current user list in account: {:}|{:}.".format(add_user.__name__, account, user_list_account)
    print(log_msg)
    logger.info(log_msg)
    conf_obj["accounts"][account_ask]["users"] = list(set(user_list_account + user_set))
    conf_obj["accounts"][account_ask]["users"].sort(key=str.lower)
    log_msg = "{:}; Result user list in account: {:}|{:}.".format(add_user.__name__, account, conf_obj["accounts"][account_ask]["users"])
    print(log_msg)
    logger.info(log_msg)

    return conf_obj


def get_contracts(logger: Logger, api_host: str, req_obj: Session, account: dict):
    contract_list = list()
    account_ask = account["ask"]
    account_name = account["name"]
    api_method = "GET"
    api_uri = "/papi/v1/contracts"
    api_url = "https://{:}{:}".format(api_host, api_uri)
    api_params = dict()
    if account_ask != "N/A":
        api_params["accountSwitchKey"] = account_ask
    else:
        pass
    api_headers = {
        "PAPI-Use-Prefixes": "true",
        "accept": "application/json",
    }

    try:
        rsp_obj_json = {
            "Type": "429 Too Many Requests",
            "Title": "Too Many Requests",
            "Detail": "You have exhausted your API Request Quota. Retry after: 10 seconds."
        }

        rsp_obj = req_obj.request(method=api_method, url=api_url, params=api_params, headers=api_headers)
        while rsp_obj.status_code == 429:
            rsp_obj_json = rsp_obj.json()
            rsp_obj_json_detail = rsp_obj_json["Detail"]
            retry_time = re.search(r"Retry after: (\d+) seconds", rsp_obj_json_detail).group(1)
            sleep_time = int(retry_time) + 2
            log_msg = "{:}; {:}; Rate limited, sleep for {:} seconds.".format(get_slot_enrollments.__name__, rsp_obj_json_detail, sleep_time)
            print(log_msg)
            logger.info(log_msg)
            time.sleep(sleep_time)
            rsp_obj = req_obj.request(method=api_method, url=api_url, params=api_params, headers=api_headers)
        else:
            pass
        if 200 <= rsp_obj.status_code <= 299:
            rsp_obj_json = rsp_obj.json()
            for item in rsp_obj_json["contracts"]["items"]:
                contract_list.append(item["contractId"])
            conf_obj[account_ask] = contract_list
            log_msg = "{:}; Add account with contracts: {:}|{:}: {:}".format(get_contracts.__name__, account_ask, account_name, contract_list)
            logger.info(log_msg)
        else:
            log_msg = "{:}; {:}: {:}: {:}".format(get_contracts.__name__, rsp_obj.status_code, account_name, rsp_obj.text)
            raise Exception(log_msg)
    except Exception as e:
        log_msg = "{:}; There is an exception: ".format(get_contracts.__name__)
        print("{:} {:}".format(log_msg, e))
        logger.exception(log_msg)
        contract_list.append("N/A")

    finally:
        print(log_msg)

    return contract_list


def get_slot_enrollments(logger: Logger, req_obj: Session, api_host: str, account: dict, contract_id: str, slot_result_list: list, col_names: list):
    account_ask = account["ask"]
    account_name = account["name"]
    account_users = account["users"]

    api_method = "GET"
    api_uri = "/cps/v2/enrollments"
    api_url = "https://{:}{:}".format(api_host, api_uri)
    api_headers = {
        "accept": "application/vnd.akamai.cps.enrollments.v11+json",
    }
    api_params = dict()
    try:
        if contract_id != "N/A":
            contract_id = contract_id.replace("ctr_", "")
            api_params["contractId"] = contract_id,
        if account_ask != "N/A":
            api_params["accountSwitchKey"] = account_ask
        else:
            pass

        rsp_obj = req_obj.request(method=api_method, url=api_url, params=api_params, headers=api_headers)
        while rsp_obj.status_code == 429:
            rsp_obj_json = rsp_obj.json()
            rsp_obj_json_detail = rsp_obj_json["Detail"]
            retry_time = re.search(r"Retry after: (\d+) seconds", rsp_obj_json_detail).group(1)
            sleep_time = int(retry_time) + 2
            log_msg = "{:}; {:}; Rate limited, sleep for {:} seconds.".format(get_slot_enrollments.__name__, rsp_obj_json_detail, sleep_time)
            print(log_msg)
            logger.warn(log_msg)
            time.sleep(sleep_time)
            rsp_obj = req_obj.request(method=api_method, url=api_url, params=api_params, headers=api_headers)
        else:
            pass
        if 200 <= rsp_obj.status_code <= 299:
            rsp_obj_json = rsp_obj.json()
            if len(rsp_obj_json["enrollments"]) == 0:
                log_msg = "{:}; No slots in contract: {:}|{:}".format(get_slot_enrollments.__name__, account_name, contract_id)
                print(log_msg)
                logger.info(log_msg)
            else:
                for enrollment in rsp_obj_json["enrollments"]:
                    if len(enrollment["pendingChanges"]) == 0:
                        slot_id = enrollment["assignedSlots"][0]
                        slot_cn = enrollment["csr"]["cn"]
                        log_msg = "{:}; No pending changes in slot: {:}|{:}".format(get_slot_enrollments.__name__, slot_id, slot_cn)
                        print(log_msg)
                        logger.info(log_msg)
                        continue
                    else:
                        for pending_change in enrollment["pendingChanges"]:
                            if ("changeType" in pending_change.keys()):
                                slot_enroll_id = enrollment["id"]
                                slot_id = enrollment["assignedSlots"][0]
                                slot_cn = enrollment["csr"]["cn"]
                                slot_type = pending_change["changeType"]
                                slot_expire_time_str, slot_left_day_str = get_slot_expire(logger=logger, account=account, slot_enroll_id=slot_enroll_id, slot_cn=slot_cn, slot_id=slot_id, req_obj=req_obj, api_host=api_host)
                                slot_result = {
                                    col_names[0]: account_name,
                                    col_names[1]: account_ask,
                                    col_names[2]: contract_id,
                                    col_names[3]: slot_cn,
                                    col_names[4]: slot_enroll_id,
                                    col_names[5]: slot_id,
                                    col_names[6]: slot_expire_time_str,
                                    col_names[7]: slot_left_day_str,
                                    col_names[8]: slot_type,
                                    col_names[9]: account_users,
                                }
                                slot_result_list.append(slot_result)
                                log_msg = "{:}; Add enrollment from contract: {:}|{:}: {:}|{:}|{:}|{:}|{:}".format(get_slot_enrollments.__name__, account_name, contract_id, slot_id, slot_cn, slot_type, slot_expire_time_str, slot_left_day_str)
                                print(log_msg)
                                logger.info(log_msg)
                            else:
                                continue
        else:
            log_msg = "{:}; {:}: {:}|{:}: {:}".format(get_slot_enrollments.__name__, rsp_obj.status_code, account_name, contract_id, rsp_obj.text)
            raise Exception(log_msg)
    except Exception as e:
        log_msg = "{:}; There is an exception: ".format(get_slot_enrollments.__name__)
        print("{:} {:}".format(log_msg, e))
        logger.exception(log_msg)

    return slot_result_list


def get_slot_expire(logger: Logger, account: dict, slot_enroll_id: str, slot_id: int, slot_cn: str, req_obj: Session, api_host: str):
    slot_expire_time_str = "N/A"
    slot_left_day_str = "N/A"
    account_ask = account["ask"]
    account_name = account["name"]

    api_method = "GET"
    api_uri = "/cps/v2/enrollments/{:}/history/certificates".format(slot_enroll_id)
    api_url = "https://{:}{:}".format(api_host, api_uri)
    api_headers = {
        "accept": "application/vnd.akamai.cps.certificate-history.v2+json",
    }
    api_params = dict()
    if account_ask != "N/A":
        api_params["accountSwitchKey"] = account_ask
    else:
        pass
    rsp_obj = req_obj.request(method=api_method, url=api_url, params=api_params, headers=api_headers)
    while rsp_obj.status_code == 429:
        log_msg = "{:}; {:}".format(get_slot_expire.__name__, rsp_obj.text)
        print(log_msg)
        logger.warn(log_msg)
        rsp_obj_json = rsp_obj.json()
        rsp_obj_json_detail = rsp_obj_json["Detail"]
        retry_time = re.search(r"Retry after: (\d+) seconds", rsp_obj_json_detail).group(1)
        sleep_time = int(retry_time) + 2
        log_msg = "{:}; Rate limited, sleep for {:} seconds.".format(get_slot_enrollments.__name__, sleep_time)
        print(log_msg)
        logger.info(log_msg)
        time.sleep(sleep_time)
        rsp_obj = req_obj.request(method=api_method, url=api_url, params=api_params, headers=api_headers)
    else:
        pass
    if 200 <= rsp_obj.status_code <= 299:
        rsp_obj_json = rsp_obj.json()
        if len(rsp_obj_json["certificates"]) == 0:
            log_msg = "{:}; No change history in certificate: {:}|{:}".format(get_slot_expire.__name__, slot_id, slot_cn)
        else:
            # expiry example: 2024-05-09T03:30:14Z
            slot_expire_time_str = rsp_obj_json["certificates"][0]["primaryCertificate"]["expiry"]
            slot_expire_time_dt = datetime.strptime(slot_expire_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            slot_left_time_delta = slot_expire_time_dt - datetime.now(tz=timezone.utc)
            slot_expire_time_str = slot_expire_time_dt.strftime("%Y-%m-%d %H:%M:%S")
            slot_left_day_str = slot_left_time_delta.days
            log_msg = "{:}; Slot expire: {:}|{:}|{:}|{:}".format(get_slot_expire.__name__, slot_id, slot_cn, slot_expire_time_str, slot_left_day_str)
        print(log_msg)
        logger.info(log_msg)
    else:
        log_msg = "{:}; {:}: {:}|{:}: {:}".format(get_slot_expire.__name__, rsp_obj.status_code, account_name, slot_id, rsp_obj.text)
        raise Exception(log_msg)
    return slot_expire_time_str, slot_left_day_str


def get_users(logger: Logger, conf_obj: dict, account: dict):
    account_ask = account
    user_list_account = conf_obj["accounts"][account_ask]["users"]

    log_msg = "{:}; User list: {:}".format(get_users.__name__, user_list_account)
    print(log_msg)
    logger.info(log_msg)

    return user_list_account


def init_col_names():
    csv_headers = [
        "Account Name",
        "Account Switch Key",
        "Contract",
        "Common Name",
        "Enrollment ID",
        "Slot ID",
        "Expire Time (UTC)",
        "Day Left",
        "Change Type",
        "Users",
    ]

    return csv_headers


def init_date():
    date_dt = datetime.now()
    date_str = datetime.strftime(date_dt, "%Y%m%d")

    return date_str


def init_edgerc(logger: Logger, path_dict: dict, conf_obj: dict):
    path_edgerc = path_dict["edgerc"]
    edgerc_section = conf_obj["api_client"]["section"]
    edgerc_obj = EdgeRc(path_edgerc)
    api_host = edgerc_obj.get(section=edgerc_section, option="host")
    log_msg = "{:}; Conf: {:} loaded, Api client section: {:}".format(init_edgerc.__name__, path_edgerc, edgerc_section)
    print(log_msg)
    logger.info(log_msg)

    return edgerc_obj, edgerc_section, api_host


def init_log(path_dict: dict):
    # Log path
    path_log_dir = path_dict["log_dir"]
    if not path_log_dir.exists():
        log_msg = "{:}; Log folder:{:} not exist, create one.".format(init_log.__name__, path_log_dir)
        path_log_dir.mkdir()
    else:
        log_msg = "{:}; Log folder:{:} exist, create skipped.".format(init_log.__name__, path_log_dir)
        pass
    print(log_msg)
    logger = logging.getLogger(__file__)
    path_log = path_dict["log"]
    logging.basicConfig(filename=path_log, encoding='utf-8', level=logging.INFO, format='%(asctime)s; %(levelname)s; %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger.info(log_msg)
    log_msg = "{:}; Log Path is: {:}".format(init_log.__name__, path_log)
    print(log_msg)
    logger.info(log_msg)

    return logger


def init_path():
    # Initial paths
    date_str = init_date()
    conf_name_dir = "conf"
    conf_name = "conf.json"
    edgerc_name = ".edgerc"
    log_name_dir = "log"
    log_name = "cps_monitor_{:}.log".format(date_str)
    output_name_dir = "output"
    output_csv_name = "result_{:}.csv".format(date_str)
    output_json_name = "result_{:}.json".format(date_str)

    path_file = Path(__file__)
    path_bin = path_file.parent
    path_root = path_bin.parent
    path_home = Path.home()
    path_conf_dir = path_root.joinpath(conf_name_dir)
    path_conf = path_conf_dir.joinpath(conf_name)
    path_edgerc = path_home.joinpath(edgerc_name)
    path_log_dir = path_root.joinpath(log_name_dir)
    path_log = path_log_dir.joinpath(log_name)
    path_output_dir = path_root.joinpath(output_name_dir)
    path_output_csv = path_output_dir.joinpath(output_csv_name)
    path_output_json = path_output_dir.joinpath(output_json_name)

    path_dict = {
        "home": path_root,
        "conf": path_conf,
        "conf_dir": path_conf_dir,
        "edgerc": path_edgerc,
        "log": path_log,
        "log_dir": path_log_dir,
        "output_csv": path_output_csv,
        "output_json": path_output_json,
        "output_dir": path_output_dir,
    }

    return path_dict


def init_request(logger: Logger, path_dict: dict, conf_obj: dict):
    edgerc_obj, edgerc_section, api_host = init_edgerc(logger=logger, path_dict=path_dict, conf_obj=conf_obj)
    req_obj = Session()
    req_obj.auth = EdgeGridAuth.from_edgerc(rcinput=edgerc_obj, section=edgerc_section)

    return req_obj, api_host


def optimize_conf(logger: Logger, path_dict: dict, conf_obj: dict):
    path_conf = path_dict["conf"]

    for ask in conf_obj["accounts"].keys():
        conf_obj["accounts"][ask]["users"].sort()

    conf_obj_pd = pandas.DataFrame.from_dict(conf_obj["accounts"])
    conf_obj_pd = conf_obj_pd.T.sort_values(by=["name"], key=lambda col: col.str.lower()).T

    conf_obj["accounts"] = conf_obj_pd.to_dict()
    with open(path_conf, mode="w+", encoding="utf-8", errors="ignore") as conf_file:
        conf_file.write(json.dumps(conf_obj, ensure_ascii=False, indent=4))

    log_msg = "{:}; Conf: {:} saved.".format(optimize_conf.__name__, path_conf)

    return log_msg


def processor_accounts(logger: Logger, path_dict: dict, conf_obj: dict, command_type: str, account_list: list):
    if command_type not in ["add", "remove"]:
        log_msg = "{:}; Invalid command: {:}".format(processor_accounts.__name__, command_type)
    else:
        if command_type == "add":
            for account in account_list:
                conf_obj = add_accounts(logger=logger, conf_obj=conf_obj, account=account)
        elif command_type == "remove":
            for account in account_list:
                conf_obj = remove_accounts(logger=logger, conf_obj=conf_obj, account=account)

        processor_conf(logger=logger, path_dict=path_dict, conf_action="save", conf_obj=conf_obj)
        log_msg = "{:}; Accounts processed: {:}".format(processor_accounts.__name__, account_list)

    return log_msg


def processor_conf(logger: Logger, path_dict: dict, conf_action: str, conf_obj: dict = dict()):
    try:
        path_conf = path_dict["conf"]
        if conf_action == "load":
            if (not path_conf.exists):
                log_msg = "{:}; Conf: {:} not exist, exit.".format(processor_conf.__name__, path_conf)
                print(log_msg)
                logger.error(log_msg)
                exit()

            with open(file=path_conf, mode="r", encoding="utf-8", errors="ignore") as conf_file_obj:
                conf_file_str = conf_file_obj.read()
                conf_file_json = json.loads(conf_file_str)
                conf_file_obj.close()

            # Set log level, default to WARNING
            # https://docs.python.org/3/library/logging.html#levels
            log_level = logging.WARNING
            if ("level" not in conf_file_json["log"].keys()):
                pass
            else:
                log_level_conf = int(conf_file_json["log"]["level"])
                if log_level_conf in [
                    logging.INFO,
                    logging.WARNING,
                    logging.ERROR,
                    logging.CRITICAL
                ]:
                    log_level = log_level_conf
                else:
                    pass
            log_msg = "{:}; Set log level to: {:}".format(processor_conf.__name__, log_level)
            logger.setLevel(log_level)
            log_msg = "{:}; Conf: {:} loaded.".format(processor_conf.__name__, path_conf)
            print(log_msg)
            logger.info(log_msg)

            return conf_file_json, logger
        elif conf_action == "save":
            log_msg = optimize_conf(logger=logger, path_dict=path_dict, conf_obj=conf_obj)
            print(log_msg)
            logger.info(log_msg)
    except Exception as e:
        log_msg = "{:}; There is an exception:".format(processor_conf.__name__, )
        print("{:} {:}".format(log_msg, e))
        logger.exception(log_msg)


def processor_slot(logger: Logger, path_dict: dict, conf_obj: dict):
    req_obj, api_host = init_request(logger=logger, path_dict=path_dict, conf_obj=conf_obj)
    slot_result_list = list()
    col_names = init_col_names()
    for account_ask in conf_obj["accounts"].keys():
        account_name = conf_obj["accounts"][account_ask]["name"]
        account_users = conf_obj["accounts"][account_ask]["users"]
        account = {
            "ask": account_ask,
            "name": account_name,
            "users": account_users,
        }
        # contract_list = get_contracts(logger=logger, api_host=api_host, req_obj=req_obj, account=account)
        # if contract_list[0] == "N/A":
        #     log_msg = "{:}; Errors when get contract list: {:}|{:}".format(processor_slot.__name__, account_ask, account_name)
        #     logger.warning(log_msg)
        # else:
        #     for contract_id in contract_list:
        #         slot_result_list = get_slot_enrollments(logger=logger, req_obj=req_obj, api_host=api_host, account=account, contract_id=contract_id, slot_result_list=slot_result_list, col_names=col_names)
        #     log_msg = "{:}; Slots processed: {:}|{:}".format(processor_slot.__name__, account_ask, account_name)
        #     logger.info(log_msg)
        slot_result_list = get_slot_enrollments(logger=logger, req_obj=req_obj, api_host=api_host, account=account, contract_id="N/A", slot_result_list=slot_result_list, col_names=col_names)
        log_msg = "{:}; Slots processed: {:}|{:}.".format(processor_slot.__name__, account_ask, account_name)
        logger.info(log_msg)
        print(log_msg)

    result_writer_slot(logger=logger, path_dict=path_dict, slot_result_list=slot_result_list, col_names=col_names)

    log_msg = "{:}; Slot processing end.".format(processor_slot.__name__)

    return log_msg


def processor_users(logger: Logger, path_dict: dict, conf_obj: dict, command_type: str, user_list: list, account_list: list):
    if command_type == "add":
        for account in account_list:
            conf_obj = add_user(logger=logger, conf_obj=conf_obj, user_set=user_list, account=account)
        log_msg = "{:}; Users added: {:}".format(processor_users.__name__, user_list)
    elif command_type == "remove":
        for account in account_list:
            conf_obj = remove_user(logger=logger, conf_obj=conf_obj, user_set=user_list, account=account)
        log_msg = "{:}; Users removed: {:}".format(processor_users.__name__, user_list)
    else:
        log_msg = "{:}; Invalid command: {:}".format(processor_users.__name__, command_type)
    print(log_msg)
    logger.info(log_msg)
    processor_conf(logger=logger, path_dict=path_dict, conf_action="save", conf_obj=conf_obj)
    log_msg = "{:}; Users processed: {:}|{:}".format(processor_users.__name__, account_list, user_list)

    return log_msg


def remove_user(logger: Logger, conf_obj: dict, user_set: set, account: dict):
    account_ask = account
    user_list_account = conf_obj["accounts"][account_ask]["users"]
    log_msg = "{:}; Current user list in account: {:}|{:}.".format(remove_user.__name__, account, user_set)
    print(log_msg)
    logger.info(log_msg)
    for user in user_set:
        user_list_account.remove(user)
    conf_obj["accounts"][account_ask]["users"] = user_list_account
    log_msg = "{:}; Result user list in account: {:}|{:}.".format(remove_user.__name__, account, conf_obj["accounts"][account_ask]["users"])
    print(log_msg)
    logger.info(log_msg)

    return conf_obj


def remove_accounts(logger: Logger, conf_obj: dict, account: str):
    account_ask = account
    account_name = conf_obj["accounts"][account_ask]["name"]
    if account_ask not in conf_obj["accounts"].keys():
        log_msg = "{:}; Account not exist: {:}|{:} ".format(remove_accounts.__name__, account_ask, account_name)
    else:
        conf_obj["accounts"].pop(account_ask)
        log_msg = "{:}; Account removed: {:}|{:}".format(remove_accounts.__name__, account_ask, account_name)

    print(log_msg)
    logger.info(log_msg)

    return conf_obj


def result_writer_slot(logger: Logger, path_dict: dict, slot_result_list: list, col_names: list):
    if len(slot_result_list) == 0:
        log_msg = "{:}; No pending enrollments in confured accounts, exit.".format(result_writer_slot.__name__)
        print(log_msg)
        logger.info(log_msg)
        exit()
    else:
        path_output_dir = path_dict["output_dir"]
        if (path_output_dir.exists()):
            log_msg = "{:}; Output dir: {:} exist, create skipped.".format(result_writer_slot.__name__, path_output_dir)
        else:
            log_msg = "{:}; Output dir: {:} not exist, create one.".format(result_writer_slot.__name__, path_output_dir)
            path_output_dir.mkdir()
        print(log_msg)
        logger.info(log_msg)

        slot_result_pd = pandas.DataFrame.from_dict(slot_result_list)
        col_names_sort = [col_names[0], col_names[6]]
        slot_result_pd = slot_result_pd.sort_values(by=col_names_sort, key=lambda col: col.str.lower())
        # print(slot_result_pd)

        path_output_json = path_dict["output_json"]
        pandas.DataFrame.to_json(slot_result_pd.T, path_output_json, index=False, indent=4)

        path_output_csv = path_dict["output_csv"]
        pandas.DataFrame.to_csv(slot_result_pd, path_output_csv, index=False)

        log_msg = "{:}; Output JSON: {:}, CSV: {:}.".format(result_writer_slot.__name__, path_output_json, path_output_csv)
    print(log_msg)
    logger.info(log_msg)

    return


def get_version():
    version = "Akamai CPS monitor {:}".format("v0.0.5")

    return version


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog='Akamai CPS monitor', description="Monitoring Akamai CPS enrollments.")
    arg_parser.add_argument("-a", "--accounts", dest="accounts", nargs="+", type=str, help="Account switch keys and account name. Format: \"ask^name\". Default: None.")
    arg_parser.add_argument("-u", "--users", dest="users", nargs="+", type=str, help="User IDs. Default: None.")
    arg_parser.add_argument("-c", "--command", dest="command", type=str, default="add", help="Values: [add|remove]. Default: add.")
    arg_parser.add_argument("-s", "--slot", dest="slot", action="store_true", help="List enrolling slots. No arguments required.")
    arg_parser.add_argument("-o", "--optimize", dest="optimize", action="store_true", help="Optimize the accounts and user order in conf file. No arguments required.")
    arg_parser.add_argument("-v", "--version", action="version", version=get_version())

    args = arg_parser.parse_args()
    if (args.accounts or args.slot or args.optimize):
        path_dict = init_path()
        logger = init_log(path_dict=path_dict)
        conf_obj, logger = processor_conf(logger=logger, path_dict=path_dict, conf_action="load")
        if (args.accounts or args.users):
            if args.accounts:
                if (not args.users):
                    result_processor = processor_accounts(logger=logger, path_dict=path_dict, conf_obj=conf_obj, command_type=args.command, account_list=args.accounts)
                else:
                    result_processor = processor_users(logger=logger, path_dict=path_dict, conf_obj=conf_obj, command_type=args.command, user_list=args.users, account_list=args.accounts)
            else:
                pass
        elif args.slot:
            result_processor = processor_slot(logger=logger, path_dict=path_dict, conf_obj=conf_obj)
        elif args.optimize:
            result_processor = optimize_conf(logger=Logger, path_dict=path_dict, conf_obj=conf_obj)
        else:
            pass
        print(result_processor)
        logger.info(result_processor)
    else:
        arg_parser.print_help()
