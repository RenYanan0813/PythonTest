#c:/python36/

#-*- coding: utf-8 -*-

__author__ = "renyanan"

import pymysql

#  第一步
'''
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='ryn812373')
cursor = db.cursor()
cursor.execute('Select version()')
data = cursor.fetchall()
print("databases version:",data)
cursor.execute("create database spiders DEFAULT CHARACTER SET utf8")
db.close()
'''

# 第二步
'''
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='ryn812373', database='spiders')
cursor = db.cursor()
sql = 'create table if not exists student(id VARCHAR(255) NOT NULL, name VARCHAR(255) not NULL , age INT NOT NULL , PRIMARY KEY (id))'
cursor.execute(sql)
db.close()
'''


'''
这样的写法烦琐而且不直观，所以我们选择直接用格式化符%s来实现。
有几个Value写几个%s，我们只需要在execute()方法的第一个参数传入该SQL语句
，Value值用统一的元组传过来就好了。这样的写法既可以避免字符串拼接的麻烦，
又可以避免引号冲突的问题。之后值得注意的是，
需要执行db对象的commit()方法才可实现数据插入，
这个方法才是真正将语句提交到数据库执行的方法。
对于数据插入、更新、删除操作，都需要调用该方法才能生效。
接下来，我们加了一层异常处理。如果执行失败，
则调用rollback()执行数据回滚，相当于什么都没有发生过。
这里涉及事务的问题。事务机制可以确保数据的一致性，
也就是这件事要么发生了，要么没有发生。比如插入一条数据，
不会存在插入一半的情况，要么全部插入，要么都不插入，
这就是事务的原子性。另外，事务还有3个属性——一致性、隔离性和持久性
。这4个属性通常称为ACID特性，具体如下表所示。
'''
#第三步
'''
id = '20120001'
user = 'Bob'
age = 20

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='ryn812373', database='spiders')
cursor = db.cursor()
sql = 'insert into students(id, name, age) VALUES (%s, %s, %s)'
try:
    cursor.execute(sql，(id, user, age))
    db.commit()
except:
    db.rollback()
'''

#第四步
'''
在很多情况下，我们要达到的效果是插入方法无需改动，
做成一个通用方法，只需要传入一个动态变化的字典就好了。
比如，构造这样一个字典：
{
    'id': '20120001',
    'name': 'Bob',
    'age': 20
}
然后SQL语句会根据字典动态构造，元组也动态构造，
这样才能实现通用的插入方法。所以，这里我们需要改写一下插入方法：
'''

#第五步
'''
data = {
    'id':"21222233",
    'name':'ryn',
    'age': 32
}
table = 'student'
keys = ','.join(data.keys())
values = ','.join(['%s'] * len(data))

sql = 'insert into {table} ({key}) VALUES ({value})'.format(table=table, key=keys, value=values)

db = pymysql.connect(host='127.0.0.1', user='root', password='ryn812373', port=3306, db='spiders')

cursor = db.cursor()
try:
    if cursor.execute(sql, tuple(data.values())):
        print("success")
        db.commit()
except:
    print('failed!')
    db.rollback()

db.close()
'''


"""
ON DUPLICATE KEY UPDATE
"""
'''
数据更新操作实际上也是执行SQL语句，最简单的方式就是构造一个SQL语句，
然后执行：sql = 'UPDATE students SET age = %s WHERE name = %s'
try:
   cursor.execute(sql, (25, 'Bob'))
   db.commit()
except:
   db.rollback()
db.close()
这里同样用占位符的方式构造SQL，
然后执行execute()方法，传入元组形式的参数，
同样执行commit()方法执行操作。如果要做简单的数据更新的话，
完全可以使用此方法。但是在实际的数据抓取过程中，
大部分情况下需要插入数据，但是我们关心的是会不会出现重复数据，
如果出现了，我们希望更新数据而不是重复保存一次。
另外，就像前面所说的动态构造SQL的问题，
所以这里可以再实现一种去重的方法，如果数据存在，则更新数据；
如果数据不存在，则插入数据。另外，这种做法支持灵活的字典传值。示例如下：




这里构造的SQL语句其实是插入语句，
但是我们在后面加了ON DUPLICATE KEY UPDATE。
这行代码的意思是如果主键已经存在，就执行更新操作。
比如，我们传入的数据id仍然为20120001，但是年龄有所变化，
由20变成了21，此时这条数据不会被插入，而是直接更新id为20120001的数据。
完整的SQL构造出来是这样的：
INSERT INTO students(id, name, age) VALUES (%s, %s, %s) 
ON DUPLICATE KEY UPDATE id = %s, name = %s, age = %s这里就变成了6个%s。
所以在后面的execute()方法的第二个参数元组就需要乘以2变成原来的2倍。
如此一来，我们就可以实现主键不存在便插入数据，存在则更新数据的功能了。

'''

#第六步
'''
data = {
    'id': '20120001',
    'name': 'Bob',
    'age': 223
}

table = 'student'
keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))

sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)


update1 = ','.join(["{key1} = %s".format(key1=key) for key in data])

sql += update1

db = pymysql.connect(host='127.0.0.1', user='root', password='ryn812373', port=3306, db='spiders')
cursor = db.cursor()

try:
    if cursor.execute(sql, tuple(data.values())*2):
        print('Successful')
        db.commit()
except:
    print('Failed')
    db.rollback()
db.close()
'''


#第七步  删除
"""
table = 'student'
condition = 'like name = "ry%"'
sql = 'delete from {table} WHERE {condition}'.format(table=table, condition=condition)

db = pymysql.connect(host='127.0.0.1', user='root', password='ryn812373', port=3306, db='spiders')
cursor = db.cursor()

try:
    cursor.execute(sql)
    db.commit()
except:
    print('failed')
    db.rollback()

db.close()

"""


sql = 'SELECT * FROM student WHERE age = 20 ORDER BY id '

db = pymysql.connect(host='127.0.0.1', user='root', password='ryn812373', port=3306, db='spiders')
cursor = db.cursor()

try:
    cursor.execute(sql)
    count = cursor.rowcount
    print("count:", count)
    one = cursor.fetchone()
    print("one:", one)
    result = cursor.fetchall()
    print("result:", result)
    print("one type:", type(one))
    for i in range(len(one)):
        print("one 元素 %s"% i, one[i])
except:
    print("error")


