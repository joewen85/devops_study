# -*- coding: utf-8 -*-
# @Time    : 2019-08-18 16:16
# @Author  : Joe
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @function: xxxxx

from django.urls import path, re_path
from .views import *

app_name = 'workorder'
urlpatterns = [
    path('apply/', WorkOrderApplyView.as_view(), name='apply'),
    path('list/', WorkOrderListView.as_view(), name='list'),
    path('history/', WorkorderHistoryView.as_view(), name='history'),
    re_path('detail/(?P<pk>[0-9]+)?/$', WorkorderDetailView.as_view(), name='detail'),

]