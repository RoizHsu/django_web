from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.

class TitleAnnouncement(models.Model):
    title = models.CharField(max_length=200, verbose_name='公告標題')
    announcement = CKEditor5Field('公告內容', config_name='default')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='發布時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    repair_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="發布人工程師", null=True, blank=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'

    def __str__(self):
        return self.title
        
    
    def get_repair_user_name(self):
        """取得維修工程師姓名"""
        if self.repair_user:
            if hasattr(self.repair_user, 'profile') and self.repair_user.profile.user_name:
                return self.repair_user.profile.user_name
            return self.repair_user.username
        return "未指定"