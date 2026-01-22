from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import TitleAnnouncement

@admin.register(TitleAnnouncement)
class TitleAnnouncementAdmin(ImportExportModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'get_repair_user_name', 'id')
    search_fields = ('title', 'repair_user__username', 'repair_user__profile__user_name')
    ordering = ('-id',)

    def get_repair_user_name(self, obj):
        """顯示發布人工程師姓名"""
        return obj.get_repair_user_name()
    get_repair_user_name.short_description = '發布人工程師'