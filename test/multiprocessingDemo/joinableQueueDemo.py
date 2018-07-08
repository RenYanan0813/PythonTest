#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"
'''
JoinableQueue就像是一个Queue对象，
    但队列允许项目的使用者通知生成者项目已经被成功处理。
    通知进程是使用共享的信号和条件变量来实现的。

构造方法：JoinableQueue([maxsize])

    maxsize：队列中允许最大项数，省略则无大小限制。

实例方法

JoinableQueue的实例p除了与Queue对象相同的方法之外还具有：

    task_done()：使用者使用此方法发出信号，
        表示q.get()的返回项目已经被处理。
        如果调用此方法的次数大于从队列中删除项目的数量，
        将引发ValueError异常
    join():生产者调用此方法进行阻塞，
        直到队列中所有的项目均被处理。
        阻塞将持续到队列中的每个项目均调用q.task_done（）方法为止

'''

from multiprocessing import Process, JoinableQueue
import time, random, os


def custom(q):
    while True:
        time.sleep(1)
        a = q.get()
        print("消费者%s拿到了%s"% (os.getpid(),a))
        q.task_done()

def product(seq, q):
    for item in seq:
        time.sleep(random.randrange(1, 2))
        q.put(item)
        print("生产者0000 %s做好了%s"%(os.getpid(),item))
    q.join()

def product1(seq, q):
    for item in seq:
        time.sleep(random.randrange(1, 2))
        q.put(item)
        print("生产者1111 %s做好了%s" % (os.getpid(), item))
    q.join()


if __name__ == "__main__":
    q = JoinableQueue()

    seq = ('产品%s'% i for i in range(10))
    p = Process(target=custom, args=(q,))
    p1 = Process(target=custom, args=(q,))
    p1.daemon = True
    p.daemon = True
    p1.start()
    p.start()
    product(seq, q)

    print("主线程")
