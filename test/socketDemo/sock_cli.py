#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

'''
这段Python代码会连接到服务器端，
然后启动两个A、B线程。
A不停写入字符“a”到Socket，一次写入32k；
B每隔1秒钟写入字符“b”到Socket，每次写入10字节。

A、B两个线程共享了同一个Socket，
每次写入都是“完整的数据包”，
Python的sendall方法会保证整个数据块完整的写入到Socket中。

问题：服务器端收到的是什么？
'''

from __future__ import print_function
import socket
# import thread
import threading
import time
import multiprocessing
import sys


def send_thread(sock, data,  times):
    ch, count  = data
    msg = ch * count
    while True:
        sock.sendall(msg)
        print("send %s * %d" % (ch, count))
        if times > 0:
            time.sleep(times)

def main():
    address = (sys.argv[1], 3000)
    message = [('a', 32768), ('b', 10)]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.connect(address)
    threading._start_new_thread(send_thread, (s, message[0], 0, ))
    threading._start_new_thread(send_thread, (s, message[1], 1, ))

    while True:
        time.sleep(20)

if __name__ == "__main__":
    main()