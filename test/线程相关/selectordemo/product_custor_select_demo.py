# -*- coding:utf-8 -*-
"""
    author: rony
"""

import queue
import threading


q = queue.Queue()


def product(name):
    count = 0

    while count <= 10:
        q.put(count)
        print("...... %s正在生产，第 %s 产品....."%(name, count))
        count += 1


def custor(name):
    count = 0

    while count <= 10:
        q.get(count)
        print("####### %s正在eatting，第 %s 产品 ######"%(name, count))
        count += 1

productors = [str("productor" + str(p)) for p in range(10)]
custors = [str("custors" + str(c)) for c in range(10)]

p_threading = []
c_threading = []

# for p in range(len(productors)):
#     p_threading.append(threading.Thread(target = product, args=(productors[p])))
#
# for c in range(len(custors)):
#     c_threading.append(threading.Thread(target = custor, args=(custors[c])))
#
# for p in range(len(productors)):
#     p_threading[p].start()
#
# for c in range(len(custors)):
#     c_threading[c].start()
#
# for p in range(len(productors)):
#     p_threading[p].join()
#
# for c in range(len(custors)):
#     c_threading[c].join()

p_threading = threading.Thread(target = product, args=(productors[1],))
c_threading = threading.Thread(target = custor, args=(custors[2],))

p_threading.start()
c_threading.start()

p_threading.join()
c_threading.join()