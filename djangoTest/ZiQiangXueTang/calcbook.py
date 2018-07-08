from __future__ import unicode_literals
#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"
from ZiQiangXueTang.wsgi import * #必须加的
from calc.models import Book

author_name_list = ['WeizhongTu', 'twz915', 'dachui', 'zhe', 'zhen']
def create_bookname():
    for i in range(1000):
        # book = Book.objects.get_or_create()
        book = Book()
        book.book_name = 'book %s' %i
        book.save()


if __name__ == "__main__":
    create_bookname()
