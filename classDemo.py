#-*- coding:utf-8 -*-

#	'类的练习'

class Student(object):

	"""docstring for Student"""
	def __init__(self, name, age):
		self.name = name
		self.age = age

	def ptsd1(std):
		print('%s: %s' %(std.name, std.age))

if __name__ == '__main__':
	student1 = Student('renyn','24')
	Student.ptsd1(student1)
