#c:/python36/
#-*- ecoding:utf-8 -*-


from random import randint
from timeit import timeit



def filterdemo(dt):
	a = filter(lambda x: x>0, dt)





if __name__ == '__main__':
	data = [randint(-10, 10) for a in range(10)]
	timeit filter(lambda x: x>0, data)