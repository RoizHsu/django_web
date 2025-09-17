from django.apps import AppConfig


class RepairConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repair'
    verbose_name = '維修'
    #verbose_name顯示名稱
    #接者要去/__init__.py低下新增如:
    #default_app_confing = 'repair.app.RepairConfig'
