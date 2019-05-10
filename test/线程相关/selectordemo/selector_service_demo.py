# -*- coding:utf-8 -*-
"""
    author: rony
"""


import selectors #基于select模块实现IO多路复用，建议使用

import socket

sock = socket.socket()
sock.bind('127.0.0.1', 8800)
sock.listen(4)
sock.setblocking(False)
sel = selectors.DefaultSelector()#根据平台选择最佳的IO多路机制，比如linux就会选择epoll


def read(conn, mask):
    try:
        data = conn.recv(1024)
        pass
    except:
        pass



while True:
    print("waitting ...")
    events = sel.select()  #[(sock) ，（），（） ] 监听

    for key, mask in events:
        # print(key.data) #accept 找出有活动的绑定函数
        # print(key.fileobj) #sock 找出有活动的文件描述符
        func = key.data
        obj = key.fileobj

        func(obj, mask)




