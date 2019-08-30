from django.db import models
from users.models import UserProfile

# Create your models here.


class Cmdb(models.Model):
    users = models.ForeignKey(UserProfile, verbose_name="客户名", on_delete=models.DO_NOTHING)

