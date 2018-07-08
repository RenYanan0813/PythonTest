#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import pickle

a = dict(name='renyn', age=32, psw=123)
f = open('./dump.txt','wb')
pickle.dump(a, f)
f.close()