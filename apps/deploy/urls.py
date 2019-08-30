# -*- coding: utf-8 -*-
# @Time    : 2019/8/25 2:25 PM
# @Author  : Joe
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @function: xxxxx

from django.urls import path, re_path
from .views import DeployApplyView,DeployProjectVersionView, DeployApplyList, DeployProjectBranchView, DeployDetailView, DeployHistoryView

app_name = 'deploy'
urlpatterns = [
    path('apply/', DeployApplyView.as_view(), name='apply'),
    path('list/', DeployApplyList.as_view(), name='list'),
    path('project_version/', DeployProjectVersionView.as_view(), name='project_versions'),
    path('project_branch/', DeployProjectBranchView.as_view(), name='project_branch'),
    path('history/', DeployHistoryView.as_view(), name='history'),
    re_path('deploy/(?P<pk>[0-9]+)?/$', DeployDetailView.as_view(), name='deploy'),
]
