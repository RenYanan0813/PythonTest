#c:/python36/

#-*- coding: utf-8 -*-

__author__ = "renyanan"

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('add', views.index, name='add2'),

    #在home.html中以{% url 'add3' 4 5 %}的形式，来在name='add3'不改变时，url怎么变都没问题
    url(r'^new_add/(\d+)/(\d+)/$', views.oldToNewAdd, name='add3'),

    #以" add2/?a=3&b=4 样式"
    url(r'^add/$', views.add, name='add'), #这样是没问题的啊
    #以" add2/333/444/ 样式"
    path('add2/<int:a>/<int:b>/', views.add2, name='add2'),

]

urlpatterns += [
    path('view1', views.view(views.view1)),
    path('view2', views.view(views.view1)),
    path('view_cache', views.view_cache)
]