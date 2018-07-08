#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

'''
多线程模式适合IO密集型运算，
这里我要使用sleep来模拟一下慢速的IO任务。
同时为了方便编写命令行程序，
这里使用Google fire开源库来简化命令行参数处理。


我们看到计算总共花费了大概5s，
总共sleep了10s由两个线程分担，所以是5s。
读者也许会问，为什么输出乱了，
这是因为print操作不是原子的，
它是两个连续的write操作合成的，
第一个write输出内容，第二个write输出换行符，
write操作本身是原子的，但是在多线程环境下，
这两个write操作会交错执行，所以输出就不整齐了。
如果将代码稍作修改，将print改成单个write操作，
输出就整齐了(关于write是否绝对原子性还需要进一步深入讨论)
# 分割子任务
def each_task(index):
    time.sleep(1)  # 睡1s，模拟IO
    import sys
    sys.stdout.write("thread %s square %d\n" % (threading.current_thread().ident, index))
    return index * index  # 返回结果

'''

import time
import fire
import threading
from concurrent.futures import ThreadPoolExecutor, wait




from concurrent.futures import ThreadPoolExecutor, wait
import fire
import time
import threading

def th_task(index):
    time.sleep(1)
    print("thread %s square %s" %(threading.current_thread().ident, index))
    return index

def run(threadnum, tasknum):
    executor = ThreadPoolExecutor(threadnum)
    start = time.time()
    fs = []
    for i in range(tasknum):
        print("......%s....", i)
        fs.append(executor.submit(th_task, i))
    wait(fs)
    end = time.time()
    timecha = end - start
    cousum = sum([f.result() for f in fs])

    executor.shutdown()
    print("sum = %s .... time %s" %(cousum, timecha))


if __name__ == "__main__":
    run(10, 10)









