from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from utils.aliyun_api import AliyunApi
from utils.tencentyun_api import TencentYun_api
from devops_study import settings


class CmdbListView(LoginRequiredMixin, PaginationMixin, TemplateView):
    login_url = '/login/'
    template_name = 'cmdb/cmdb_list.html'
    paginate_by = 20
    region = "cn-shanghai"

    def get_context_data(self, **kwargs):
        context = {}
        # get ali asset
        ali = AliyunApi(settings.AliYun_AK, settings.AliYun_SK, self.region)
        context['ali'] = ali.get_describe_instances()
        # for i in data_json['Instances']['Instance']:
        #     context.append(i)

        # get tencent asset
        tencent = TencentYun_api(settings.TencentYun_AK, settings.TencentYun_SK)
        context['tencent'] = tencent.get_describe_instances('ap-guangzhou')
        return context
