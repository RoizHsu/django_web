from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import UserMaterial
# Register your models here.


@admin.register(UserMaterial)
class UserMaterialAdmin(ImportExportModelAdmin):
    list_display = ('office','ext','name','share','PC_ID','ip','PC','LCD','MacAddress')
    search_fields = ('office','ext','name','share','PC_ID','ip','PC','LCD','MacAddress')#搜尋
    list_filter=('ext','name')#過濾
    ordering=('id',)
