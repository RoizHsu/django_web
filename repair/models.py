from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Location(models.Model):
    name = models.CharField(verbose_name="位置",max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "位置"

class Job_title(models.Model):
    name = models.CharField(verbose_name="職稱",max_length=10)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "職稱"

class State(models.Model):
    name = models.CharField(verbose_name="狀態",max_length=5)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "狀態"

class Repair(models.Model):
    ip = models.CharField(verbose_name="IP",max_length=255)
    ext = models.IntegerField(verbose_name="分機")
    name = models.CharField(verbose_name="叫修人",max_length=10)
    share = models.CharField(verbose_name="股別",max_length=255)
    jt = models.ForeignKey(verbose_name="職稱", to=Job_title, on_delete=models.CASCADE)
    repair_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="維修工程師", null=True, blank=True)
    location = models.ForeignKey(verbose_name="位置", to=Location, on_delete=models.CASCADE)
    F = models.IntegerField(verbose_name="樓層", default=0)
    office = models.CharField(verbose_name="科室",max_length=255)
    Q = models.TextField(verbose_name="報修問題")
    A = models.TextField(verbose_name="回復報修")
    state = models.ForeignKey(verbose_name="狀態", to=State, on_delete=models.CASCADE)
    start = models.DateTimeField(verbose_name="維修時間", default=timezone.now)#每次更新就會更新時間
    finish = models.DateTimeField(verbose_name="維修結束", null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_repair_user_name(self):
        """取得維修工程師姓名"""
        if self.repair_user:
            if hasattr(self.repair_user, 'profile') and self.repair_user.profile.user_name:
                return self.repair_user.profile.user_name
            return self.repair_user.username
        return "未指定"
    
    class Meta:
        verbose_name_plural = "維修單"

