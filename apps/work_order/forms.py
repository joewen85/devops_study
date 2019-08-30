# -*- coding: utf-8 -*-
# @Time    : 2019-08-18 21:08
# @Author  : Joe
# @Site    :
# @File    : forms.py
# @Software: PyCharm
# @function: xxxxx

from django import forms
from .models import WorkOrder
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class WorkOrderAddForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': '标题不能为空',
            'max_length': '标题超过100个字符'})
    # order_contents = forms.CharField(required=True)
    order_contents = RichTextUploadingFormField(required=True)
    orderfiles = forms.FileField(required=False)
