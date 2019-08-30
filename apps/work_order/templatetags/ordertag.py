# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 18:18
# @Author  : Joe
# @Site    : 
# @File    : ordertag.py
# @Software: PyCharm
# @function: xxxxx

from django import template

register = template.Library()

@register.filter(name='orderfile_name')
def orderfile_name(file_path):

    file_name = str(file_path).split('/')[-1]
    return file_name