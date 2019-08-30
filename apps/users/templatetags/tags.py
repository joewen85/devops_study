# -*- coding: utf-8 -*-
# @Time    : 2019-08-11 15:49
# @Author  : Joe
# @Site    : 
# @File    : tags.py
# @Software: PyCharm
# @function: xxxxx

from django import template

register = template.Library()


@register.filter(name='bool2str')
def bool2str(value):
    if value:
        return u'是'
    else:
        return u'否'


@register.filter(name='group_list')
def groups_str2(group_list):
    if len(group_list) < 3:
        return ''.join(group.name for group in group_list)
    else:
        return '%s ...' % ''.join(group.name for group in group_list[0:2])


@register.filter(name='member_str')
def member_str(member_list):
    if len(member_list) < 3:
        return ''.join(member.name for member in member_list)
    else:
        return '%s ...' % ' '.join(member.name for member in member_list[0:2])

@register.filter(name='perm_str')
def perm_str(perm_list):
        if len(perm_list) < 3:
            return ''.join(permname.codename for permname in perm_list)
        else:
            return '%s ...' % ' '.join([permname.codename for permname in perm_list[0:2]])
