#-*- coding:utf-8 -*-

#	'类的练习'

class Student(object):
	count = 0
	"""docstring for Student"""
	def __init__(self, name, age):
		self.name = name
		self.age = age
		self.count += 1

	def ptsd1(std):
		print('%s: %s' %(std.name, std.age))

#测试 if语句外的return为何取决于if语句执行后的结果
def abc(a):
	if a > 4:
		return a
	else:
		return 0
	return 10


if __name__ == '__main__':
	"""
	student1 = Student('renyn','24')
	#Student.ptsd1(student1) #ptsd1测试
	student2 = Student('ryn','23')
	#print(Student.count)
	#dir(student1)

	print(abc(0))  #abc()测试
	"""

	""" 序列化 pickle
	
	import pickle
	d = dict(name='Bob', age=20, score=88)
	#print(pickle.dumps(d)) #转成bytes

	#pickle.dump()写入
	f = open("dump.txt", "wb")
	pickle.dump(d, f) #将转化的bytes存到f（dump.txt）下
	f.close()	
	
	#pickle.load() 读出
	当我们要把对象从磁盘读到内存时，
	可以先把内容读到一个bytes，
	然后用pickle.loads()方法反序列化出对象，
	也可以直接用pickle.load()方法
	从一个file-like Object中直接反序列化出对象。
	
	f1 = open("dump.txt", "rb")
	d1 = pickle.load(f1) #  pickle.load() 与pickle.loads()区别
	f1.close()
	#print(type(d1))  # <class 'dict'>
	print(d1)
	"""

	"""
	JSON 格式化
	如果我们要在不同的编程语言之间传递对象，
	就必须把对象序列化为标准格式，比如XML，
	但更好的方法是序列化为JSON，
	因为JSON表示出来就是一个字符串，
	可以被所有语言读取，
	也可以方便地存储到磁盘或者通过网络传输。
	JSON不仅是标准格式，并且比XML更快，
	而且可以直接在Web页面中读取，非常方便。
	"""
	"""
	import json
	d2 = dict(name='Rob', age=330, score=818)
	j = json.dumps(d2)  #将str转换为json
	print(j)  
	"""


	"""
		re 练习：
		1. 邮箱匹配 :  r'^[0-9a-zA-Z]{5}@(163|qq|126|gmail)(.com)$'
		2. 优化一： r'^\w+@(\w+)(.\w+)$', 不严谨
			优化二： r'^\w+@(\w+)(.[a-zA-Z]+)$'
		3. \w 匹配 [0-9a-zA-Z]
		   \d 匹配 [0-9]

	"""

	import re

	r1 = r'^\w+@(\w+)(.[a-zA-Z]+)$'
	r2 = input("输入一个邮箱: ")
	#r2 = "1e2@163.com"
	r3 = re.match(r1, r2)

	
	print(r3)
	print(r3.groups())
	print(r3.group(0))
	print(r3.group(1))
		