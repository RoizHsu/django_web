from django.db import models
from django.utils import timezone
# Create your models here.


class Location(models.Model):#位置
    name = models.CharField(verbose_name="位置",max_length=255)##位置
    def __str__(self):
        return self.name  # 顯示
    class Meta:
        verbose_name_plural = "位置"
        # verbose_name_plural = ""顯示APP名稱

class Job_title(models.Model):#職稱
    name = models.CharField(verbose_name="職稱",max_length=10)
    def __str__(self):
        return self.name  # 顯示
    class Meta:
        verbose_name_plural = "職稱"
        # verbose_name_plural = ""顯示APP名稱


class RepairUser(models.Model):#維修人員
    name = models.CharField(verbose_name="工程師",max_length=255)
    def __str__(self):
        return self.name  # 顯示
    class Meta:
        verbose_name_plural = "維修工程師"
        # verbose_name_plural = ""顯示APP名稱


class State(models.Model):
    name = models.CharField(verbose_name="狀態",max_length=5)
    def __str__(self):
        return self.name  # 顯示
    class Meta:
        verbose_name_plural = "狀態"
        # verbose_name_plural = ""顯示APP名稱


class Repair(models.Model):
    ip = models.CharField(verbose_name="IP",max_length=255)  # IP  #verbose_name=""顯示名稱
    ext = models.IntegerField(verbose_name="分機")  # 分機
    name = models.CharField(verbose_name="叫修人",max_length=10)#叫修人
    share = models.CharField(max_length=255)#股別
    jt = models.ForeignKey(Job_title, on_delete=models.CASCADE)#職稱
    repairUser = models.ForeignKey(RepairUser, on_delete=models.CASCADE)#維修人
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # 位置
    F = models.IntegerField(default=0)#樓
    office = models.CharField(max_length=255)#科室
    Q = models.CharField(max_length=255)#原因
    A = models.CharField(max_length=255)#回答
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    start = models.DateTimeField(default=timezone.now)#開始#default=timezone.now預設時間現在
    finish = models.DateTimeField()#結束
    def __str__(self):
        return self.name  # 顯示
    class Meta:
        verbose_name_plural = "維修單"
        # verbose_name_plural = ""顯示APP名稱

