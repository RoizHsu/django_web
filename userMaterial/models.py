from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class UserMaterial(models.Model):
    office = models.CharField(verbose_name="辦公室",max_length=255)#使用科室
    ext = models.IntegerField(verbose_name="分機")#分機
    name = models.CharField(verbose_name="使用者",max_length=10) #使用者
    share = models.CharField(verbose_name="股別",max_length=5)  # 股別
    Job_title = models.CharField(verbose_name="職稱",max_length=10)#職稱
    PC_ID = models.CharField(verbose_name="電腦名稱",max_length=255)#電腦名稱
    ip = models.CharField(verbose_name="IP",max_length=255)#ip
    PC = models.CharField(verbose_name="電腦型號",max_length=255)#PC
    LCD = models.CharField(verbose_name="螢幕型號",max_length=255)#LCD
    MacAddress = models.CharField(max_length=255)#mac
    dey = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name  # 顯示
    class Meta:
        verbose_name_plural = "使用者"