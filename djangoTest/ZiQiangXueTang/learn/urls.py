#c:/python36/

#-*- coding: utf-8 -*-

__author__ = "renyanan"

from django.urls import path, include
from . import views
urlpatterns = [
    path('index', views.home, name='index'),
]