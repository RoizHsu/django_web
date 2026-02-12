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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """自定義 Django Admin 後台的外鍵欄位下拉選單顯示格式
        
        作用：讓管理員在後台選擇「發布人工程師」時，同時看到姓名和帳號，方便識別
        
        運作原理：
        1. 當 Admin 表單遇到 ForeignKey 欄位時，Django 會自動呼叫此方法
        2. 我們針對 'repair_user' 欄位進行特殊處理
        3. 透過 label_from_instance 自定義顯示邏輯
        4. 優先顯示「真實姓名 (帳號)」格式，例如：「王小明 (wangxiaoming)」
        5. 如果沒有 profile 或 user_name，則僅顯示 username
        
        參數說明：
        - db_field: 資料庫欄位物件（這裡是 repair_user）
        - request: HTTP 請求物件（可用於權限判斷）
        - **kwargs: 其他參數
        
        使用情境：管理員在 Admin 後台新增/編輯公告時，選擇發布人更直觀
        """
        if db_field.name == 'repair_user':
            # 修改下拉選單中每個選項的顯示文字
            field = super().formfield_for_foreignkey(db_field, request, **kwargs)
            # lambda obj: 為每個 User 物件定義顯示文字的規則
            # f-string 格式化為「姓名 (帳號)」的形式
            field.label_from_instance = lambda obj: ( #自定義顯示邏輯
                f"{obj.profile.user_name} ({obj.username})" 
                if hasattr(obj, 'profile') and obj.profile.user_name 
                else obj.username
            )
            return field
        # 其他 ForeignKey 欄位使用預設行為
        return super().formfield_for_foreignkey(db_field, request, **kwargs)