# encoding=utf-8
from cps_monitor import path_init, date_init, log_init, config_processor
import requests
import pandas
from pathlib import Path

# Home path, log, config init
path_home = path_init()
date_str = date_init()
logger = log_init()

try:
    # Load result file
    filename_csv = "result_{:}.csv".format(date_str)
    name_csv_folder = "output"
    path_csv_file = path_home.joinpath(name_csv_folder).joinpath(filename_csv)
    # Check file
    if not Path(path_csv_file).exists():
        log_msg = "webex_sender; check_file; File:{:} not exist, exit.".format(path_csv_file)
        print(log_msg)
        logger.error(log_msg)
        exit()

    # Check data
    pd_dataframe = pandas.read_csv(path_csv_file)
    if len(pd_dataframe) == 0:
        log_msg = "webex_sender; check_data; No enrollment data in file: {:}, exit.".format(path_csv_file)
        print(log_msg)
        logger.error(log_msg)
        exit()

    msg_header = "Dear team, here is the enrollment pending list of {:}:".format(date_str)
    pd_markdown = pd_dataframe.to_markdown(index=False)
    msg_body = "```\n{:}\n```".format(pd_markdown)
    msg_full = "{:}\n\n{:}".format(msg_header, msg_body)
    print(msg_full)

    # Load spaces
    config_obj = config_processor(logger=logger, config_action="load")
    webex_auth_token = config_obj["webex"]["auth"]["token"]
    webex_spaces = config_obj["webex"]["spaces"]
    webex_spaces_name = list()
    if len(webex_spaces) == 0:
        log_msg = "webex_sender; load_space; Webex spaces: NONE! Exit."
        print(log_msg)
        logger.error(log_msg)
        exit()
    else:
        webex_spaces_name = list(webex_spaces.keys())
        webex_spaces_name.sort(key=str.lower)
        log_msg = "webex_sender; load_space; Webex spaces: {:}".format(webex_spaces_name)
        print(log_msg)
        logger.info(log_msg)

    # Requests: Send result to spaces
    req_obj = requests.Session()
    for webex_space_name in webex_spaces_name:
        webex_space_id = webex_spaces[webex_space_name]
        api_method = "POST"
        api_host = "webexapis.com"
        api_uri = "/v1/messages"
        api_url = "https://{:}{:}".format(api_host, api_uri)
        api_params = {
        }
        api_headers = {
            "Authorization": "Bearer {:}".format(webex_auth_token),
            "accept": "application/json",
        }
        api_payload = {
            "roomId": webex_space_id,
            "markdown": msg_full,
        }

        try:
            rsp_obj = req_obj.request(method=api_method, url=api_url, params=api_params, data=api_payload, headers=api_headers)
            if rsp_obj.status_code == 200:
                rsp_obj_json = rsp_obj.json()
                log_msg = "webex_sender; message_send; Send success to space: {:}".format(webex_space_name)
                logger.info(log_msg)
            else:
                log_msg = "webex_sender; message_send; Send failed to space: {:}".format(webex_space_name)
                raise Exception(log_msg)
        except Exception as e:
            log_msg = e
            logger.error(log_msg)
        finally:
            print(log_msg)
except Exception as e:
    log_msg = e
    print(log_msg)
    logger.error(log_msg)
