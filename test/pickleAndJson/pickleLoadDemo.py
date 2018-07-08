#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import pickle
f = open('./dump.txt', 'rb')
print(pickle.load(f))
f.close()

