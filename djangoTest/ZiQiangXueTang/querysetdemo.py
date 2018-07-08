#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

from ZiQiangXueTang.wsgi import *
from blog.models import Article, Author, Tag

#查看 Django queryset 执行的 SQL
print(str(Author.objects.all().query))
print(str(Author.objects.filter(name="Weizhong").query))

# values_list 获取元组形式结果
authors = Author.objects.values_list('name', 'qq')
print(authors)
print(list(authors))

#如果只需要 1 个字段，可以指定 flat=True
print(Author.objects.values_list('name', flat=True))

print(list(Author.objects.values_list('name', flat=True)))

print(Article.objects.filter(author__name='twz915').values_list('title', flat=True))


#values 获取字典形式的结果
print(Author.objects.values('name', 'qq'))
print( list(Author.objects.values('name', 'qq')))
print(Article.objects.filter(author__name='twz915').values('title'))

'''
注意：

1. values_list 和 values 返回的并不是真正的 列表 或 字典，
也是 queryset，他们也是 lazy evaluation 的（惰性评估，通俗地说，
就是用的时候才真正的去数据库查）

2. 如果查询后没有使用，在数据库更新后再使用，
你发现得到在是新内容！！！如果想要旧内容保持着，数据库更新后不要变，
可以 list 一下

3. 如果只是遍历这些结果，
没有必要 list 它们转成列表（浪费内存，数据量大的时候要更谨慎！！！）
'''

'''
select_related 优化一对一，多对一查询

开始之前我们修改一个 settings.py 让Django打印出在数据库中执行的语句

settings.py 尾部加上
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}

这样当 DEBUG 为 True 的时候，我们可以看出 django 执行了什么 SQL 语句
'''