# -*- coding: utf-8 -*-
# @Time    : 2019-08-05 14:31
# @Author  : Joe
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
# @function: xxxxx
import re
from django.core import validators
from django import forms
from django.contrib.auth.models import Group, Permission
from .models import UserProfile



class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    password = forms.CharField(required=True, min_length=6)


# 添加用户表单验证
class UserProfileForm(forms.ModelForm):
    # phone = forms.CharField(max_length=11, messages='请出入正确格式的号码！')
    # pwd1 = forms.CharField(max_length=16, min_length=6)
    # pwd2 = forms.CharField(max_length=16, min_length=6)


    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'phone']
        error_messages = {
            'username': {
                'unique': '用户名已存在'
            }
        }

    def clean_phone(self):
        """
        通过正则表达式验证手机号码是否合法
        """
        phone = self.cleaned_data['phone']
        phone_regex = r'1[345678]\d{9}'
        p = re.compile(phone_regex)
        if p.match(phone):
            return phone
        else:
            raise forms.ValidationError('手机号码非法', code='invalid')


class UpdateForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    name = forms.CharField(max_length=32, required=True)
    phone = forms.CharField(max_length=11, required=True)
    email = forms.EmailField()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_regex = r'^1[34578][0-9]{9}$'
        p = re.compile(phone_regex)
        if p.match(phone):
            return phone
        else:
            raise forms.ValidationError('手机号码非法', code='invalid')


class PasswordForm(forms.Form):
    pwd1 = forms.CharField(max_length=16, min_length=6)
    pwd2 = forms.CharField(max_length=16, min_length=6)

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('pwd1')
        pwd2 = cleaned_data.get('pwd2')
        if pwd1 != pwd2:
            raise forms.ValidationError("两次输入密码不一致", code='invalid')
        return cleaned_data
