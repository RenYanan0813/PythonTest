#-*- coding: utf-8 -*-

def diGui(x):
	#if x == 1:
		#return 1
	n = 1    # n=1 ，0 为什么不一样呢？
	if x > 0:
		n = x * diGui(x-1) 
	return n

if __name__ == '__main__':
	print(diGui(5))


