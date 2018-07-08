#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import json

a = '11111111112ssswwr'

f = open('./jsonDump.text', 'w')

json.dump(a, f)

f.close()