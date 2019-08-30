# -*- coding: utf-8 -*-
# @Time    : 2019-08-23 15:15
# @Author  : Joe
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @function: xxxxx

from django.urls import path
from .views import CmdbListView

app_name = 'cmdb'
urlpatterns = [
    path('list/', CmdbListView.as_view(), name='list')
]