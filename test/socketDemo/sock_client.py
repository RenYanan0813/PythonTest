#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.setsockopt()
client.connect(('127.0.0.1', 8001))


while True:
    cli_data = input()
    client.send("hello server, i am sending mes! {}".format(cli_data).encode("utf8"))
    # client.send(cli_data.encode("utf8"))
    data = client.recv(1024)
    print(data.decode("utf8"))
client.close()