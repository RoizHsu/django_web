from django.contrib import admin
from .models import UserProfile

# 自定義顯示方式
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birthday', 'created_at')  # 顯示欄位
    search_fields = ('user__username', 'phone')  # 搜尋欄位
    list_filter = ('birthday',)  # 過濾器
    ordering = ('-created_at',)  # 排序（最新的在前）

# 註冊模型到後台
admin.site.register(UserProfile, UserProfileAdmin)
