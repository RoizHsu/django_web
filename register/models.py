from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone


class Job_Positions(models.Model):
    name = models.CharField(verbose_name="員工職稱",max_length=10)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "員工職稱"

class Department(models.Model):
    name = models.CharField(verbose_name="部門名稱",max_length=10)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "部門名稱"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='姓名')
    identity = models.CharField(max_length=10, blank=True, null=True,unique=True, verbose_name='身份證字號')
    department = models.ForeignKey(to=Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='員工部門')
    jobp = models.ForeignKey(to=Job_Positions, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='員工職稱')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='地址')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='電話')
    email = models.EmailField(max_length=254, blank=True, null=True, unique=True, verbose_name='電子郵件')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='薪資')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='到職日期')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    group = models.ForeignKey(
        Group,#抓取Django內建的群組模型
        on_delete=models.SET_NULL,#移除UER時，將群組設為空值且不刪除群組
        null=True, #允許群組欄位為空值
        blank=True, #允許表單提交時群組欄位為空值
        verbose_name='權限群組')
    def save(self, *args, **kwargs):
        # 在保存用戶資料時，同步更新關聯的 User 模型的 Group群組和 Email
        super().save(*args, **kwargs)
        if self.group:
            self.user.groups.clear()  # 清除現有的群組
            self.user.groups.add(self.group)  # 添加新的群組
        else:
            self.user.groups.clear()  # 如果沒有指定群組，則清除USER所有群組
        if self.email:      
            self.user.email = self.email
            self.user.save(update_fields=['email'])

    class Meta:
        verbose_name = '用戶資料'
        verbose_name_plural = '用戶資料'

    def __str__(self):
        return f"{self.user.username} 的個人資料"
    
class Calendar_Shift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendars')
    title = models.CharField(max_length=100, verbose_name='事件標題')
    description = models.TextField(blank=True, null=True, verbose_name='事件描述')
    start_time = models.DateTimeField(verbose_name='開始時間', help_text="0-23")
    end_time = models.DateTimeField(verbose_name='結束時間',help_text="0-23")

    class Meta:
        verbose_name = '員工行事曆'
        verbose_name_plural = '員工行事曆'

    def __str__(self):
        return f"{self.user.username} 行事曆: {self.title}"