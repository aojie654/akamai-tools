# encoding=utf-8

import json
from bs4 import BeautifulSoup
from pathlib import Path

import requests

# fip = Path("/Users/sao/Downloads/dnschecker.org.html")
# with open(file=fip, mode="r", encoding="utf-8", errors="ignore") as fio:
#     hc = fio.read()

fop = Path(__file__).parents[1].joinpath("conf").joinpath("dns_tmp.json")
req_url = "https://dnschecker.org/"
req_method = "GET"
req_params = {}
req_payload = {}
req_headers = {
    "authority": "dnschecker.org",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "Chromium;v=118, Google Chrome;v=118, Not=A?Brand;v=99",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
}

rep_obj = requests.request(method=req_method, url=req_url, params=req_params, data=req_payload, headers=req_headers)
if rep_obj.status_code != 200:
    print_msg = "Error: {:}".format(rep_obj.text)
    print(print_msg)
else:
    hc = rep_obj.text
    soup = BeautifulSoup(hc, "lxml")
    tb_t = soup.find("tbody")
    dns_result = {
        "local": {
            "DNS": "local",
            "Location": "Local ISP",
            "Provider": "Local ISP"
        }
    }
    for tr_t in tb_t:
        if tr_t.name != "tr":
            continue
        else:
            dns_dns, dns_location, dns_provider = tr_t.contents[1].i["data-clipboardtext"], tr_t["data-location"], tr_t["data-provider"]
            dns_result[dns_dns] = {
                "DNS": dns_dns,
                "Location": dns_location,
                "Provider": dns_provider,
            }
            print_msg = json.dumps(obj=dns_result[dns_dns], ensure_ascii=False, indent=4)
            print(print_msg)

    with open(file=fop, mode="w+", encoding="utf-8", errors="ignore") as foo:
        dns_json = json.dumps(obj=dns_result, ensure_ascii=False, indent=4)
        foo.write(dns_json)

    print_msg = "DNS result saved to: {:}".format(fop)
    print(print_msg)
