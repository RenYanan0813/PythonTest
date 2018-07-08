#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

from urllib.parse import urlparse
import socket

def get_url(url):
    #通过socket请求http
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 80))

    useragent = "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0"
    client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n{}\r\n\r\n".format(path, host, useragent).encode("utf8"))

    data = b""

    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break

    data = data.decode("utf8")
    http_data = data.split("\r\n\r\n")[1] #截取掉响应头
    print(http_data)

    client.close()


if __name__ == "__main__":
    get_url("htttps://www.baidu.com")