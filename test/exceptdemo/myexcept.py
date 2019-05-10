# -*- coding:utf-8 -*-
"""
    author: rony
"""

class MyExcept(Exception):
    pass


def foo(num):
    if (num == 0):
        raise MyExcept("except %s"% num)

foo(0)