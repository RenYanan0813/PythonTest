from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse #可以重定向，即是点击原来旧的地址直接跳转到新地址

# Create your views here.

def index(request):
    return render(request, "home.html" , {"v":"hello"})

#获取 add/?a=3&b=4 形式的url的值
def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))

#获取 add/3/4/ 形式的url的值
def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))

#可以重定向，即是点击原来旧的地址直接跳转到新地址
def oldToNewAdd(request, a, b):
    return HttpResponseRedirect(reverse('add2', args=(a, b)))

def view1(request):
    pass

def view2(request):
    pass

def view(fun):
    def views(request):

        return  fun
    return views

from .models import *
from django.core.cache import cache #django提供的缓存

'''
#自带小缓存
def view_cache(request):
    if cache.get("book"):
        b = cache.get("book")
    else:
        b = Book.objects.all()
        cache.set("book",b)
    return render_to_response("1.html", {"book": b})

'''

#针对视图的缓存
from django.views.decorators.cache import cache_page
#设置装饰器， 在15分钟后缓存过期
@cache_page(60 * 15)
def view_cache(request):
    b = Book.objects.all()
    return render_to_response("1.html", {"book":b})
    

