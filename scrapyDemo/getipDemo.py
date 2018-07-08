#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import base64, requests, time, re

base_url = 'http://192.168.1.108'
user = 'TP-LINK_90_601'
pwd = '15021224148'

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Referer': base_url + '/userRpm/StatusRpm.htm',
    'Cookie': 'Authorization=Basic ' + base64.b64encode((user + ':' + pwd).encode(encoding='utf-8')).decode(
        encoding='utf-8')
}


def get_ip():
    url = "http://2018.ip138.com/ic.asp"
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    return ip


def get_ip_status():
    url = base_url + "/userRpm/StatusRpm.htm"
    r = requests.get(url=url, headers=headers)
    pattern = re.compile('(\d+\.\d+\.\d+\.\d+)')
    ip = re.findall(pattern, r.text)
    return ip[0]


def change_ip():
    url = base_url + '/userRpm/StatusRpm.htm?Disconnect=%B6%CF%20%CF%DF&wan=1'
    requests.get(url=url, headers=headers)
    while True:
        time.sleep(5)
        new_ip = get_ip_status()
        if new_ip != '0.0.0.0':
            break


if __name__ == "__main__":
    change_ip()