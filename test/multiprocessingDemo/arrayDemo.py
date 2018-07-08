#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

'''
Array

构造方法：Array(typecode_or_type, size_or_initializer, **kwds[, lock])

    typecode_or_type：同上
    size_or_initializer：如果它是一个整数，
        那么它确定数组的长度，并且数组将被初始化为零。
        否则，size_or_initializer是用于初始化数组的序列，
        其长度决定数组的长度。
    kwds：传递给typecode_or_type构造函数的参数
    lock：同上

使用示例：
	


注意：Value和Array只适用于Process类。
'''

import multiprocessing

def f(n, a):
    n.value = 3.14
    a[0] = 5


if __name__ == '__main__':
    num = multiprocessing.Value('d', 0.0)
    arr = multiprocessing.Array('i', range(10))
    p = multiprocessing.Process(target=f, args=(num, arr))
    p.start()
    p.join()
    print(num.value)
    print(arr[:])