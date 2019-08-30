from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class UserProfile(AbstractUser):
    """
    用户类，添加name和phone字段
    """
    name = models.CharField(max_length=32, verbose_name="姓名")
    phone = models.CharField(max_length=11, verbose_name="手机号码")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['-id']
        app_label = 'users'

    def __str__(self):
        return self.username



