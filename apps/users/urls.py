# -*- coding: utf-8 -*-
# @Time    : 2019-08-05 14:09
# @Author  : Joe
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @function: xxxxx

from django.urls import path, re_path

from .views import IndexView, LogoutView, LoginView, UserList, RoleList, PermissionList, UserDetailView, ModifyPasswordView, UserPermissionView, RoleDetailView, RolePermissionView, PermissionDetailView

app_name = 'users'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('list/', UserList.as_view(), name='user_list'),
    path('role/', RoleList.as_view(), name='role_list'),
    path('permission/', PermissionList.as_view(), name='permission_list'),
    re_path('userdetail/(?P<pk>[0-9]+)?/$', UserDetailView.as_view(), name='user_detail'),
    re_path('modifypassword/(?P<uid>[0-9]+)?/$', ModifyPasswordView.as_view(), name='modify_pwd'),
    re_path('userpermission/(?P<pk>[0-9]+)?/$', UserPermissionView.as_view(), name='user_permission'),
    re_path('groupdetail/(?P<pk>[0-9]+)?/$', RoleDetailView.as_view(), name='role_detail'),
    re_path('grouppermission/(?P<pk>[0-9]+)?/$', RolePermissionView.as_view(), name='role_permission'),
    re_path('permissiondetail/(?P<pk>[0-9]+)?/$', PermissionDetailView.as_view(), name='permission_detail'),
]
