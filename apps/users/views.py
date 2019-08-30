import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from pure_pagination.mixins import PaginationMixin
from django.http import HttpResponse
from django.http import QueryDict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from .forms import LoginForm, UserProfileForm, UpdateForm, PasswordForm
from .models import UserProfile


class IndexView(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'index.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('users:index'))


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        res = {"status": 0}
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            remember = request.POST.get('remember')
            user = authenticate(**data)
            if user:
                if user.is_active == 1:
                    login(request, user)
                    res['redirect_to'] = '/'
                    if remember == 'on':
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                    # return redirect(reverse('users:index'))
                else:
                    res['status'] = 1
                    res['errmsg'] = "用户被禁用"
            else:
                res['status'] = 1
                res['errmsg'] = "用户名或密码错误"
        else:
            res['status'] = 1
            res['errmsg'] = "用户名或密码输入不合法"
        return JsonResponse(res)


# class UserList(View):
#     def get(self, request):
#         all_users = UserProfile.objects.all()
#         return render(request, 'user_list.html', {'userdatas': all_users})
#
#     def post(self, request, *args, **kwargs):
#         pass

class UserList(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = UserProfile
    template_name = 'user/user_list.html'
    paginate_by = 10
    object = UserProfile
    ordering = ['id']
    context_object_name = 'userdatas'
    keyword = ''


    def get_queryset(self):
        queryset = super(UserList, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(
                Q(username__icontains=self.keyword) | Q(name__icontains=self.keyword))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    @method_decorator(permission_required('user.add_userprofile', login_url='/', raise_exception=True))
    def post(self, request):
        _userForm = UserProfileForm(request.POST)
        _passwordForm = PasswordForm(request.POST)
        if _userForm.is_valid() and _passwordForm.is_valid():
            try:
                _passwordForm.cleaned_data['password'] = make_password(
                    _passwordForm.cleaned_data.get('pwd1'))
                _userForm.cleaned_data['is_active'] = True
                _passwordForm.cleaned_data.pop('pwd1')
                _passwordForm.cleaned_data.pop('pwd2')
                data = dict(
                    _passwordForm.cleaned_data,
                    **_userForm.cleaned_data)
                self.model.objects.create(**data)
                res = {'code': 0, 'result': '添加用户成功'}
            except BaseException:
                res = {'code': 1, 'errmsg': '添加用户失败'}
        else:
            # 聚合错误信息
            all_errors = dict(
                _userForm.errors.get_json_data(),
                **_passwordForm.errors.get_json_data())
            res = {'code': 1, 'errmsg': json.dumps(all_errors)}
        return JsonResponse(res, safe=True)

    @method_decorator(permission_required('users.delete_uesrprofile', login_url='/'))
    def delete(self, request, **kwargs):
        user_id = QueryDict(request.body).dict()
        try:
            user = UserProfile.objects.filter(pk=user_id['id']).delete()
            ret = {'code': 0, 'result': '操作成功'}
        except BaseException:
            ret = {'code': 1, 'errmsg': '操作失败'}

        return JsonResponse(ret)


class UserDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    # model name
    model = UserProfile
    # template name
    template_name = "user/user_detail.html"
    # 上下文内容对象，相当与render(request, 'user/user_detail.html',
    # context=user})。不设为object
    context_object_name = "userdata"

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        _updateForm = UpdateForm(request.POST)
        if _updateForm.is_valid():
            data = _updateForm.cleaned_data
            try:
                self.model.objects.filter(pk=pk).update(**data)
                res = {'code': 0, 'result': '修改成功！'}
            except BaseException:
                res = {'code': 1, 'errmsg': '修改失败！'}
        else:
            res = {'code': 1, 'errmsg': _updateForm.errors.as_json()}
        return JsonResponse(res)


class ModifyPasswordView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = UserProfile
    template_name = 'user/change_passwd.html'
    context_object_name = 'userdata'
    pk_url_kwarg = 'uid'

    def post(self, request, **kwargs):
        pk = request.POST.get('uid')
        _passwordForm = PasswordForm(request.POST)
        if _passwordForm.is_valid():
            password = make_password(_passwordForm.cleaned_data.get('pwd1'))
            self.model.objects.filter(pk=pk).update(password=password)
            ret = {
                'code': 0,
                'result': '修改成功',
                'next_url': '/users/userdetail/%s' % pk}
        else:
            ret = {
                'code': 1,
                'errmsg': _passwordForm.errors.as_data(),
                'next_url': '/users/userdetail/%s' % pk}
        return render(request, 'jump.html', {'ret': ret})


class UserPermissionView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = UserProfile
    template_name = 'user/user_group_power.html'
    context_object_name = 'userdatas'

    # def get_queryset(self):
    #     queryset = super(UserPermissionView, self).get_queryset()
    #     pk = self.kwargs.get('pk')
    #     queryset = self.model.objects.filter(pk=pk)
    #     print(queryset)
    #     return queryset

    def get_context_data(self, **kwargs):
        super(UserPermissionView, self).get_context_data()
        pk = self.kwargs.get('pk')
        try:
            user_info = self.model.objects.get(pk=pk)
            user_roles = user_info.groups.all()
            user_permissions = user_info.user_permissions.all()
        except BaseException:
            return JsonResponse([], safe=False)
        roles = Group.objects.all()
        permissions = Permission.objects.all()

        # get roles
        has_roles = [user_role for user_role in user_roles]
        not_roles = [role for role in roles if role not in user_roles]

        # get permissions
        has_permissions = [
            user_permission for user_permission in user_permissions]
        not_permissions = [
            permission for permission in permissions if permission not in user_permissions]

        context = {
            'userdatas': {
                'id': pk,
                'name': user_info.name,
                'user_has_groups': has_roles,
                'user_not_groups': not_roles,
                'user_has_perms': has_permissions,
                'user_not_perms': not_permissions
            }
        }
        return context

    def post(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        roles_list = request.POST.getlist('groups_selected')
        permissions_list = request.POST.getlist('perms_selected')
        user_info = self.model.objects.get(pk=pk)
        user_info.groups.set(roles_list)
        user_info.user_permissions.set(permissions_list)
        return redirect(reverse('users:user_permission', kwargs={'pk': pk}))


# class UserCreateView(LoginRequiredMixin, CreateView):
#     login_url = '/login'
#     model = UserProfile
#     template_name = 'user/useraddmodel.html'
#     form_class = UserProfileForm


class RoleList(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/login'
    model = Group
    template_name = 'groups/role_list.html'
    context_object_name = 'groupdatas'
    paginate_by = 10
    keyword = ''

    # 过滤字段，搜索功能
    def get_queryset(self):
        queryset = super(RoleList, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = self.model.objects.filter(name__icontains=self.keyword)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = super(RoleList, self).get_context_data(**kwargs)
        queryset['keyword'] = self.keyword
        print(queryset['object_list'])
        return queryset

    def post(self, request, **kwargs):
        groupname = self.request.POST.get('groupname')
        try:
            self.model.objects.create(name=groupname)
            res = {'code': 0, 'result': "添加成功"}
        except BaseException:
            res = {'code': 1, 'errmsg': "添加失败"}

        return JsonResponse(res)

    def delete(self, request, **kwargs):
        group_id = QueryDict(self.request.body).dict()
        try:
            self.model.objects.filter(id=group_id['id']).delete()
            res = {'code': 0, 'result': "删除成功"}
        except BaseException:
            res = {'code': 1, 'result': "删除失败"}
        return JsonResponse(res)


class RoleDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Group
    template_name = 'groups/role_detail.html'
    context_object_name = 'groupdatas'

    def post(self, request, **kwargs):
        group_id = self.request.POST.get('id')
        group_name = self.request.POST.get('groupname')
        try:
            self.model.objects.filter(id=group_id).update(name=group_name)
            res = {'code': 0, 'result': '修改成功'}
        except BaseException:
            res = {'code': 1, 'result': '修改失败'}
        return JsonResponse(res)


class RolePermissionView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Group
    template_name = 'groups/role_permission.html'
    context_object_name = 'groupdatas'
    # permission_required('user.view_permission', 'user.change_permission')

    def get_context_data(self, **kwargs):
        super(RolePermissionView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        group_info = self.model.objects.get(pk=pk)
        group_permissions = group_info.permissions.all()
        permissions = Permission.objects.all()

        group_has_permissions = [
            group_permission for group_permission in group_permissions]
        group_not_permissions = [
            permission for permission in permissions if permission not in group_permissions]

        # print(group_has_permissions)
        # print(group_not_permissions)

        context = {
            'groupdatas': {
                'id': pk,
                'name': group_info.name,
                'group_has_permissions': group_has_permissions,
                'group_not_permissions': group_not_permissions
            }
        }
        return context

    def post(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        permissions_id = self.request.POST.getlist('perms_selected')
        print(self.request.POST)
        try:
            self.model.objects.get(pk=pk).permissions.set(permissions_id)
            ret = {
                'code': 0,
                'result': "修改成功",
                'next_url': '/user/grouppermission/%s' % pk}
        except BaseException:
            ret = {
                'code': 1,
                'errmsg': "修改失败",
                'next_url': '/user/grouppermission/%s' % pk}
        return render(request, 'jump.html', ret)


class PermissionList(LoginRequiredMixin, PaginationMixin, ListView):
    """
    权限list获取
    """
    login_url = '/login'
    model = Permission
    context_object_name = 'permissiondatas'
    template_name = 'permission/permission_list.html'
    paginate_by = 10

    def post(self, request, **kwargs):
        querydict = self.request.POST
        print(querydict)
        return HttpResponse('ok')

class PermissionDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Permission
    context_object_name = 'permissiondatas'
    template_name = 'permission/permission_detail.html'
