#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"
"""
自定义一个过滤器
"""

from django import template
import datetime

register = template.Library()

@register.filter(name='cut')
def myCut(value, arg):
    return value.replace(arg, "!")


#自定义模板tag 解析器
#{{current_time "%Y-%m-%d %H:%M:%S"}}
@register.tag(name='current_time')
def do_current_time(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except:
        raise template.TemplateSyntaxError('syntax')
    return CurrentNode(format_string[1:-1])

class CurrentNode(template.Node):
    def __init__(self, format):
        self.format_string = str(format)

    def render(self, context):
        now = datetime.datetime.now()
        return now.strftime(self.format_string)
