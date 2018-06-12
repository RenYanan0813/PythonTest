#c:/python36/

#-*- coding: utf-8 -*-

from django.urls import path
from . import views
urlpatterns=[
    #当底层的urls下使用path('register/', df_views.register),则以下不需要了
    #当底层的urls下使用path('df_user/', include('df_user.urls')), 则以下需要
    path('register', views.register, name='register'), #正确
    path('register_handle', views.register_handle, name='register_handle')
]