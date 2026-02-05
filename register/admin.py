from django.contrib import admin
from .models import UserProfile , Job_Positions, Department

# 自定義顯示方式
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_name', 'group', 'phone', 'email', 'birthday', 'created_at')  # 顯示欄位
    search_fields = ('user__username', 'user_name', 'phone')  # 搜尋欄位
    list_filter = ('birthday',)  # 過濾器
    ordering = ('-created_at',)  # 排序（最新的在前）

@admin.register(Job_Positions)
class Job_PositionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ('id',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ('id',)

# 註冊模型到後台
admin.site.register(UserProfile, UserProfileAdmin)
