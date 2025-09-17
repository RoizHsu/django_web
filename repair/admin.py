from django.contrib import admin
from .models import Location,Repair,RepairUser,Job_title,State
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Job_title)
class Job_titleAdmin(ImportExportModelAdmin):
    list_display = ('name','id')
    ordering = ('id',)



class RepairAdmin(ImportExportModelAdmin):
    list_display = ('ip','ext','name','location','ext','id')
    search_fields = ('ip','ext','name','location','ext',)
    ordering = ('-id',)



class StateAdmin(admin.ModelAdmin):
    #list_display = ('name','id')
    ordering = ('id',)






admin.site.register(Location)
admin.site.register(RepairUser)
admin.site.register(Repair,RepairAdmin)
admin.site.register(State,StateAdmin)