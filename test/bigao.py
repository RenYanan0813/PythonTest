#-*- coding:utf-8 -*-

import logging

"""
闭包的概念

def count():
	fs = []
	for i in range(1,4):
		def f():
			return i*i
		fs.append(f)
	return fs
f1, f2, f3 = count()

"""

#斐波那契数列
class Fib(object):
	"""docstring for Fib"""
	def __init__(self):
		self.a, self.b = 0, 1

	def __iter__(self):
		return self

	def __next__(self):
		self.a, self.b = self.b, self.a + self.b
		if self.a > 10000:
			raise StopIteration()
		return self.a
		

if __name__ == '__main__':
	# for x in Fib():  #测试斐波那契数列
		# print(x)
	
	#main()
	# print(f1())
	# print(f2())
	# print(f3())
	""" try ... except... finally
	try:
		print("try...")
		r = 10/0
		print('result', r)
	except ZeroDivisionError as e:
		print('except:',e)
		logging.exception(e)  #logging 记录错误信息
	finally:
		print("finally...")
	print("end.")

	for x in range(1,10):
		#print(logging[x])

		print(x)
	"""

# io 文件操作
# 

try:
	f = open("../1.txt", "r", encoding='utf-8')
	print(f.read())
except IOError as e:
	print(e)
finally:
	f.close()
	print("...finally")