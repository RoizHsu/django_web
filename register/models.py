from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='電話')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='註冊時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    class Meta:
        verbose_name = '用戶資料'
        verbose_name_plural = '用戶資料'

    def __str__(self):
        return f"{self.user.username} 的個人資料"
