#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

class myMiddleware(object):
    def __init__(self):
        print("hello, this is my mymiddleware...")

    def process_view(self, request, func, args, kwargs):
        print(func)