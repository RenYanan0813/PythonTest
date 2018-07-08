#-*- coding:utf-8 -*-
from django.shortcuts import render, redirect
#密码加密模块
# from hashlib import sha1
import  hashlib
#改pycharm的原因，同级目录的模块不能直接导入，需加包名，服务器不会报错
#也可在df_user包点击右键--> make directory as设为资源根包,但服务器仍然不会认识，但操作字段会方便很多

from .models import UserInfo
import pymysql
# from  models import *
import json


# Create your views here.

def get_useinfo(request):
    usermess = UserInfo.objects.all()

def register(request):
    return render(request, 'df_user/register.html')

def register_handle(request):
    #接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 =  post.get('cpwd')
    uemail = post.get('email')
    #两次密码输入对比
    if upwd != upwd2:
        return redirect('/user/register/') # 重定向
    #密码加密，无法加密，报格式错
    s1 = hashlib.sha1()
    #s1.update(bytes(upwd,encoding='utf-8'))
    s1.update(upwd.encode('utf-8'))
    upwd3 = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功，转到登录界面
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname = uname).count()
    return JsonResponse({'count': count})



from django.conf import settings
from django.http import HttpResponse
def imgload(request):
    return render(request, 'loadimg.html')

def upload(request):
    if request.method == "POST":
        f1 = request.FILES['pic']
        fname = '%s/%s' % (settings.MEDIA_ROOT,f1.name)
        with open(fname, 'wb') as pic: #'w'时，读取的数据结构为str，'wb'时为byte
            for c in f1.chunks():
                pic.write(c)
        return HttpResponse("ok")
    else:
        return HttpResponse("error")


def upload1(request):
    if request.method == 'POST':
        f1 = request.FILES['pic3']
        fname = '%s/%s' % (settings.MEDIA_ROOT, f1.name)
        with open(fname, 'wb') as fp:
            for b in f1.chunks():
                fp.write(b)
        return HttpResponse("success!")
    else:
        return HttpResponse("fail....")


