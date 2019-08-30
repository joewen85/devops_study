from django.db import models
from users.models import UserProfile

# Create your models here.


class DeployModel(models.Model):
    STATUS = (
        (0, '申请'),
        (1, '审核'),
        (2, '上线'),
        (3, '取消上线'),
    )
    name = models.CharField(max_length=50, verbose_name="项目名")
    version = models.CharField(max_length=20, verbose_name="版本号")
    version_desc = models.CharField(max_length=200, verbose_name="版本描述")
    applicant = models.ForeignKey(UserProfile, verbose_name='申请人', on_delete=models.CASCADE,
                                  related_name="applicant")
    reviewer = models.ForeignKey(UserProfile, verbose_name="审核人", on_delete=models.CASCADE, blank=True, null=True, related_name='reviewer')
    handle = models.ForeignKey(UserProfile, verbose_name="最终处理人", on_delete=models.CASCADE, blank=True, null=True, related_name='handler')
    update_detail = models.CharField(max_length=200, verbose_name="更新详情")
    status = models.IntegerField(choices=STATUS, verbose_name="上线状态")
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    deploy_time = models.DateTimeField(auto_now=True, verbose_name="上线完成时间")

    class Meta:
        verbose_name = "代码发布系统"
        verbose_name_plural = verbose_name
