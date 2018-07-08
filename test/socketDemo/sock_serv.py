#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"
'''
这是一段服务器端代码，它接受客户端请求读取第一个字符，
如果是“a”则尝试读取后续的32767（32768-1）字节；
如果是“b”则读取后续的9（10-1）字节。每次读取都是“完整的”，
这一点是通过loop_read不断循环读取实现的。

客户端代码通过sendall方法能保证完整的数据交给内核，
那么服务器端收到的数据可能是32k的a或者10bytes的b。

找两台服务器分别运行服务器端和客户端（我的环境是2vCPU，1G内存）。
大概10-30秒左右，服务器端输出错误——发现“不完整的数据包”。
（输出太大，我截取其中一部分）
'''

from __future__ import print_function

import socket

def loop_read(sock, read_size):
    buf = bytearray(read_size)
    view = memoryview(buf)
    while read_size:
        nbytes = sock.recv_into(view, read_size)
        view = view[nbytes]
        read_size -= nbytes
    return buf

def client_handle(ss, a_size, b_size):
    while True:
        one = ss.recv(1)
        read_size = 1
        if one == "a":
            buf = loop_read(ss, a_size - 1)
            read_size = a_size
        else:
            buf = loop_read(ss, b_size - 1)
            read_size = b_size
        if buf.count(one) != read_size - 1:
            print(buf)
            return

def main():
    port = 3000
    address = ("0.0.0.0", port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen()

    print("start server in %d" % port)
    ss, addr = s.accept()
    print("connected from ", addr)
    client_handle(ss, 32768, 10)

if __name__ == "__main__":
    main()