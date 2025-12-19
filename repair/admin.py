from django.contrib import admin
from .models import Location, Repair, Job_title, State
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Job_title)
class Job_titleAdmin(ImportExportModelAdmin):
    list_display = ('name', 'id')
    ordering = ('id',)


class RepairAdmin(ImportExportModelAdmin):
    list_display = ('ip', 'ext', 'name', 'location', 'get_repair_user_display', 'state', 'id')
    search_fields = ('ip', 'ext', 'name', 'repair_user__username', 'repair_user__profile__user_name')
    ordering = ('-id',)
    
    def get_repair_user_display(self, obj):
        """顯示維修工程師姓名"""
        return obj.get_repair_user_name()
    get_repair_user_display.short_description = '維修工程師'


class StateAdmin(admin.ModelAdmin):
    ordering = ('id',)


admin.site.register(Location)
admin.site.register(Repair, RepairAdmin)
admin.site.register(State, StateAdmin)