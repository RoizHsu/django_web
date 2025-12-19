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
    share = models.CharField(max_length=255)
    jt = models.ForeignKey(Job_title, on_delete=models.CASCADE)
    repair_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="維修工程師", null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    F = models.IntegerField(default=0)
    office = models.CharField(max_length=255)
    Q = models.CharField(max_length=255)
    A = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    start = models.DateTimeField(default=timezone.now)
    finish = models.DateTimeField()
    
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

