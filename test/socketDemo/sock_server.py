#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import socket
import threading
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8001))
server.listen()


def handle_client(sock, addr):
    while True:
        data = sock.recv(1024)
        print("receive client data.... {}".format(data.decode("utf8")))
        ser_data = input()
        sock.send("server send to client ... {}!".format(ser_data).encode("utf8"))

while True:
    sock, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(sock, addr))
    client_thread.start()
    # if sock.shutdown(True):
    #     client_thread.join()
sock.close()
server.close()


