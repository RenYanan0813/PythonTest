#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

'''
相比多线程适合处理IO密集型任务，多进程适合计算密集型。
接下来我们要模拟一下计算密集型任务。
我的个人电脑有2个核心，正好可以体验多核心计算的优势。
那这个密集型计算任务怎么模拟呢，我们可以使用圆周率计算公式。

1/1^2  + 1/2^2  + 1/3^2  + … = π/6 

通过扩大级数的长度n，就可以无限逼近圆周率。
当n特别大时，计算会比较缓慢，
这时候CPU就会一直处于繁忙状态，这正是我们所期望的。

作者：老錢
链接：https://juejin.im/post/5b1e36476fb9a01e4a6e02e4
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''

import os
import sys
import math
import time
import fire
from concurrent.futures import ProcessPoolExecutor, wait


# 分割子任务
def each_task(n):
    # 按公式计算圆周率
    s = 0.0
    for i in range(n):
        s += 1.0/(i+1)/(i+1)
    pi = math.sqrt(6*s)
    # os.getpid可以获得子进程号
    sys.stdout.write("process %s n=%d pi=%s\n" % (os.getpid(), n, pi))
    return pi


def run(process_num, *ns):  # 输入多个n值，分成多个子任务来计算结果
    # 实例化进程池，process_num个进程
    executor = ProcessPoolExecutor(process_num)
    start = time.time()
    fs = []  # future列表
    for n in ns:
        print("......%s....", n)
        fs.append(executor.submit(each_task, int(n)))  # 提交任务
    wait(fs)  # 等待计算结束
    end = time.time()
    duration = end - start
    print ("total cost: %.2fs" % duration)
    executor.shutdown()  # 销毁进程池


if __name__ == '__main__':
    fire.Fire(run( 4, 5000000, 5001000, 5002000, 5003000))

"""
通过代码可以看出多进程模式在代码的编写上和多线程没有多大差异，
仅仅是换了一个类名，其它都一摸一样。这也是concurrent库的魅力所在，
将多线程和多进程模型抽象出了一样的使用接口。
接下来我们运行一下python p.py 1 5000000 5001000 5002000 5003000，
总共计算4次pi，只用一个进程。观察输出
process 96354 n=5000000 pi=3.1415924626
process 96354 n=5001000 pi=3.14159246264
process 96354 n=5002000 pi=3.14159246268
process 96354 n=5003000 pi=3.14159246272
total cost: 9.45s
可以看出来随着n的增大，结果越来越逼近圆周率，
因为只用了一个进程，所以任务是串行执行，总共花了大约9.5s。
接下来再增加一个进程，观察输出
> python p.py 2 5000000 5001000 5002000 5003000
process 96529 n=5001000 pi=3.14159246264
process 96530 n=5000000 pi=3.1415924626
process 96529 n=5002000 pi=3.14159246268
process 96530 n=5003000 pi=3.14159246272
total cost: 4.98s
从耗时上看缩短了接近1半，说明多进程确实起到了计算并行化的效果。
此刻如果使用top命令观察进程的CPU使用率，这两个进程的CPU使用率都占到了接近100%。
如果我们再增加2个进程，是不是还能继续压缩计算时间呢
> python p.py 4 5000000 5001000 5002000 5003000
process 96864 n=5002000 pi=3.14159246268
process 96862 n=5000000 pi=3.1415924626
process 96863 n=5001000 pi=3.14159246264
process 96865 n=5003000 pi=3.14159246272
total cost: 4.86s
看来耗时不能继续节约了，因为只有2个计算核心，
2个进程已经足以榨干它们了，即使再多加进程也只有2个计算核心可用。

作者：老錢
链接：https://juejin.im/post/5b1e36476fb9a01e4a6e02e4
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
