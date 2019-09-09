import json
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, View, ListView, DetailView
from utils.gitlab_api import GitLab_ApiV4
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DeployForm
from .models import DeployModel
from pure_pagination.mixins import PaginationMixin
from django.db.models import Q
from users.models import UserProfile
from devops_study import settings

# Create your views here.


class DeployApplyView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'deploy/deply_apply.html'

    def get_context_data(self, **kwargs):
        context = super(DeployApplyView, self).get_context_data(**kwargs)
        user = self.request.user.username

        gl = GitLab_ApiV4(settings.GITURL, settings.GIILAB_PRIVATE_TOKEN)
        user_obj = gl.get_users(user)
        # context['user_projects'] = gl.get_all_project()
        try:
            user_projects = user_obj.projects.list()

            context['user_projects'] = user_projects
        except:
            context['user_projects'] = None
        return context

    def post(self, request):
        deployform = DeployForm(request.POST)
        if deployform.is_valid():
            data = deployform.cleaned_data
            data['status'] = 0
            data['applicant'] = self.request.user
            name = data['name'].split('/')[1]
            data['name'] = name
            has_apply = DeployModel.objects.filter(name=name, status__lte=2)
            if has_apply:
                return render(request, 'deploy/deply_apply.html', {'errmsg': '该项目已经申请上线，但是上线还没有完成，上线完成后方可再次申请！'})
            try:
                DeployModel.objects.create(**data)
                return redirect(reverse('deploy:list'))
            except:
                return render(request, 'deploy/deply_apply.html', {'errmsg': '申请失败，请查看日志'})
        else:
            return render(request, 'deploy/deply_apply.html', {'forms': deployform, 'errmsg': '填写格式错误'})


class DeployProjectVersionView(LoginRequiredMixin, View):

    def get(self, request):
        project_id = request.GET.get('project_id').split('/')[0]
        project = GitLab_ApiV4(settings.GITURL, settings.GIILAB_PRIVATE_TOKEN)
        tags = project.get_project_version(int(project_id))
        tags = [[tag.name, tag.message] for tag in tags]
        # print(tags)
        return HttpResponse(json.dumps(tags),content_type='application/json')


class DeployProjectBranchView(LoginRequiredMixin, View):
    def get(self, request):
        project_id = request.GET.get('project_id').split('/')[0]
        project = GitLab_ApiV4(settings.GITURL, settings.GIILAB_PRIVATE_TOKEN)
        branchs = project.get_project_branchs(project_id)
        branchs = [[branch.name, branch.commit['message']] for branch in branchs]
        # print(branchs)
        return HttpResponse(json.dumps(branchs), content_type='application/json')


class DeployApplyList(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/login/'
    model = DeployModel
    context_object_name = 'apply_list'
    template_name = 'deploy/deployapply_list.html'
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        # queryset = super(DeployApplyList, self).get_queryset()
        user_id = self.request.user.id
        user_groups = [group.name for group in UserProfile.objects.get(pk=user_id).groups.all()]
        if self.request.user.is_superuser or ('op' in user_groups or 'test' in user_groups):
            queryset = self.model.objects.filter(status__lt=2)
        else:
            queryset = self.model.objects.filter(applicant=user_id).filter(status__lt=2)
        try:
            self.keyword = self.request.GET.get('keyword', '').strip()
            queryset = queryset.filter(Q(name__icontains=self.keyword) | Q(version__contains=self.keyword) | Q(version_desc__icontains=self.keyword))
        except Exception as e:
            print(e)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DeployApplyList, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self, request, **kwargs):
        pk = self.request.POST.get('apply_id')
        try:
            self.model.objects.filter(pk=pk).delete()
            data = {'code': 0, 'result': 'success'}
        except Exception as e:
            data = {'code': 1, 'errmsg': '取消失败'}
        return JsonResponse(data)


class DeployDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = DeployModel
    template_name = 'deploy/deploy_detail.html'
    context_object_name = 'deploy'

    def get_context_data(self, **kwargs):
        context = super(DeployDetailView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        user_groups = [group.name for group in UserProfile.objects.get(pk=user_id).groups.all()]
        if 'op' in user_groups or 'test' in user_groups:
            context['is_reviewer'] = True
        else:
            context['is_reviewer'] = False
        return context

    def post(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        user_id = self.request.user.id
        status = self.model.objects.get(pk=pk).status
        if status == 0:
            self.model.objects.filter(pk=pk).update(status=1, reviewer=user_id)
        elif status == 1:
            self.model.objects.filter(pk=pk).update(status=2, handle=user_id)
        return redirect(reverse('deploy:deploy', kwargs={'pk': pk}))


class DeployHistoryView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = DeployModel
    template_name = 'deploy/deploy_history.html'
    context_object_name = 'history_list'
    keyword = ''

    def get_queryset(self):
        # queryset = super(DeployHistoryView, self).get_queryset()
        user_id = self.request.user.id
        self.keyword = self.request.GET.get('keyword', '').strip()
        user_group_list = [group.name for group in UserProfile.objects.get(pk=user_id).groups.all()]
        # 判断用户是否超级管理员和是否op组或者test组
        if self.request.user.is_superuser or ('op' in user_group_list or 'test' in user_group_list):
            queryset = self.model.objects.filter(status__gte=2).filter(Q(name__icontains=self.keyword) | Q(version_desc__icontains=self.keyword))
        else:
            queryset = self.model.objects.filter(status__gte=2).filter(applicant=user_id).filter(Q(name__icontains=self.keyword) | Q(version_desc__icontains=self.keyword))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DeployHistoryView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context
