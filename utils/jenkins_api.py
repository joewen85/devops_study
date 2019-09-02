# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 12:33 PM
# @Author  : Joe
# @Site    : 
# @File    : jenkins_api.py
# @Software: PyCharm
# @function: xxxxx

import jenkins

from jenkins import JenkinsException
from jenkins import version
from devops_study import settings


server = jenkins.Jenkins(settings.JENKINS_URL, username=settings.JENKINS_USER_ID, password=settings.JENKINS_TOKEN, timeout=10)
# user = server.get_whoami()
# version = server.get_version()
# job_count = server.jobs_count()
# all_jobs = server.get_all_jobs()
# job = server.get_job_config('team-dividend')
# print(job)

# server.create_job('empty', jenkins.EMPTY_CONFIG_XML)
# get all jobs
jobs = server.get_jobs()

# get job config parenment: fullname return: XML config
my_job = server.get_job_config('products/backend_release')

# build project
# server.build_job('empty')

# disable project
# server.disable_job('empty')

# copy project
# server.copy_job('empty', 'empty1')

# enable project
# server.enable_job('empty')

# server.reconfig_job('empty1', jenkins.RECONFIG_XML)

# server.delete_job('empty1')
# server.delete_job('empty')
