from django.apps import AppConfig

class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'
    verbose_name = '人資資料庫'  # 設定應用程式在管理介面中的顯示名稱
