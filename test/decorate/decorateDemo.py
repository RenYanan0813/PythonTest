# -*- coding:utf-8 -*-
"""
    author: rony
"""

#定义一个简单的装饰器，并只返回内部方法run
def animal(fun):
    def run():
        print("animal running ...")

    return run


@animal
def dog():
    print("dog runned")

dog()