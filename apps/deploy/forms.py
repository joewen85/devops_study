# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 4:11 PM
# @Author  : Joe
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
# @function: xxxxx

from django import forms
from .models import DeployModel


class DeployForm(forms.ModelForm):
    class Meta:
        model = DeployModel
        fields = ['name', 'version', 'version_desc', 'update_detail']

    # def clean_name(self):
    #     context = super(DeployForm, self).clean_name()
    #     print()

