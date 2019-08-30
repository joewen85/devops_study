from django.db import models
from users.models import UserProfile
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class WorkOrder(models.Model):
    STATUS = (
        (0, '申请'),
        (1, '处理中'),
        (2, '完成'),
        (3, '失败'),

    )
    title = models.CharField(max_length=100, verbose_name="工单标题")
    # order_contents = models.TextField(verbose_name="工单内容")
    order_contents = RichTextUploadingField(verbose_name="工单内容")
    orderfiles = models.FileField(
        upload_to='orderfiles/%Y/%m',
        verbose_name="附件",
        blank=True,
        null=True)
    applicant = models.ForeignKey(
        UserProfile,
        verbose_name="申请人",
        on_delete=models.CASCADE,
        related_name='workorder_applicant')
    assign = models.ForeignKey(
        UserProfile,
        verbose_name="指派人",
        on_delete=models.CASCADE,
        related_name='workorder_assign')
    handler = models.ForeignKey(
        UserProfile,
        verbose_name="最终处理人",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='workorder_handle')
    status = models.IntegerField(
        choices=STATUS,
        default=0,
        verbose_name="工单状态")
    # result_desc = models.TextField(verbose_name="处理结果", blank=True, null=True)
    result_desc = RichTextUploadingField(verbose_name="处理结果", blank=True, null=True)
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    complete_time = models.DateTimeField(auto_now=True, verbose_name="处理完成时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'workorder'
        verbose_name_plural = verbose_name
        ordering = ['-complete_time']
