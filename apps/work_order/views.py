from django.shortcuts import render, reverse, redirect
from django.views.generic import CreateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import WorkOrder
from users.models import UserProfile
from .forms import WorkOrderAddForm
from django.http import HttpResponse, JsonResponse
from pure_pagination import PaginationMixin
from django.db.models import Q
from django.contrib.auth.models import Group
from django.http import QueryDict



class WorkOrderApplyView(LoginRequiredMixin, View):
    """
    申请工单
    """

    def get(self, request):
        op_group_members = UserProfile.objects.filter(groups__name='op')
        return render(request, 'workorder/workorderadd.html', {'op_members': op_group_members})

    def post(self, request):
        validate_form = WorkOrderAddForm(request.POST, request.FILES)
        print(request.POST)
        if validate_form.is_valid():
            print(validate_form.cleaned_data)
            title = validate_form.cleaned_data.get('title')
            order_contents = validate_form.cleaned_data.get('order_contents')
            orderfiles = validate_form.cleaned_data.get('orderfiles')
            assign = request.POST.get('assign')
            applicant = request.user

            WorkOrder.objects.create(title=title, order_contents=order_contents, orderfiles=orderfiles, assign_id=assign, applicant=applicant)
            return redirect(reverse('workorder:list'))
        else:
            return render(request, 'workorder/workorderadd.html', {'forms': validate_form, 'errmsg': '工单填写格式出错！'})


class WorkOrderListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    工单list
    """
    login_url = '/login/'
    template_name = "workorder/workorder_list.html"
    model = WorkOrder
    context_object_name = 'orderlist'
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        context = super(WorkOrderListView, self).get_queryset()
        applicant = self.request.user
        applicant_groups = [applicant_group.name for applicant_group in UserProfile.objects.get(pk=applicant.id).groups.all()]
        self.keyword = self.request.GET.get('keyword', '').strip()
        # 判断登陆用户是否op组的成员 或者 是否admin
        if 'op' in applicant_groups or applicant.username == 'admin':
            context = self.model.objects.filter(status__lt=2).filter(Q(title__icontains=self.keyword) | Q(order_contents__icontains=self.keyword) | Q(result_desc__icontains=self.keyword))
        else:
            context = self.model.objects.filter(applicant__username=applicant).filter(status__lt=2).filter(Q(title__icontains=self.keyword) | Q(order_contents__icontains=self.keyword) | Q(result_desc__icontains=self.keyword))

        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkOrderListView, self).get_context_data(**kwargs)
        group_member = [member.id for member in Group.objects.get(name='op').user_set.all()]
        if self.request.user.id in group_member:
            include_or_not = True
        else:
            include_or_not = False
        context['keyword'] = self.keyword
        context['group_member_include'] = include_or_not
        return context

    def delete(self, request, **kwargs):
        order_id = QueryDict(self.request.body).dict()['id']
        try:
            self.model.objects.get(id=order_id).delete()
            data = {'code': 0, 'result': 'success'}
        except:
            data = {'code': 1, 'errmsg': '没有这条记录'}

        return JsonResponse(data)


class WorkorderDetailView(LoginRequiredMixin,DetailView):
    """
    工单详情
    """
    login_url = '/login'
    context_object_name = 'workorder'
    template_name = 'workorder/workorder_detail.html'
    model = WorkOrder

    def post(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        order_info = self.model.objects.get(pk=pk)
        result_desc = self.request.POST.get('result_desc', '')

        if result_desc:
            order_info.status = 2
            order_info.result_desc = result_desc
        else:
            order_info.status = 1
        order_info.handler_id = self.request.user.id
        order_info.save()
        return redirect(reverse('workorder:list'))


class WorkorderHistoryView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    历史工单逻辑
    """
    login_url = '/login/'
    context_object_name = 'orderlist'
    model = WorkOrder
    template_name = 'workorder/workorder_history.html'
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        queryset = super(WorkorderHistoryView, self).get_queryset()
        appliant = self.request.user
        self.keyword = self.request.GET.get('keyword', '').strip()
        # 查询当前用户是否op组
        group_members = [group_member.id for group_member in Group.objects.get(name='op').user_set.all()]
        if appliant.id in group_members or appliant.username == 'admin':
            queryset = self.model.objects.filter(status=2).filter(Q(title__icontains=self.keyword) | Q(order_contents__icontains=self.keyword) | Q(result_desc__icontains=self.keyword))
        else:
            queryset = self.model.objects.filter(applicant=appliant.id).filter(status=2).filter(Q(title__icontains=self.keyword) | Q(order_contents__icontains=self.keyword) | Q(result_desc__icontains=self.keyword))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkorderHistoryView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context


