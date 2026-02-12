from django import forms
from django.contrib.auth.models import User
from .models import TitleAnnouncement
from django_ckeditor_5.widgets import CKEditor5Widget

#新增表單
class TitleAnnouncementForm(forms.ModelForm):
    announcement = forms.CharField(widget=CKEditor5Widget(config_name='default'))
    
    class Meta:
        model = TitleAnnouncement
        fields = ['title', 'announcement', 'repair_user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'repair_user': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        """表單初始化方法：自定義欄位顯示行為
        作用：讓前台編輯器的「發布人工程師」下拉選單顯示真實姓名而非帳號
        運作原理：
        1. 透過 label_from_instance 方法覆寫預設的顯示邏輯
        2. 優先嘗試從 User.profile.user_name 取得真實姓名
        3. 如果沒有 profile 或 user_name 為空，則顯示預設的 username (帳號)
        4. hasattr() 確保在沒有 profile 的情況下不會出錯
        使用情境：當使用者在前台編輯器選擇「發布人工程師」時，會看到「王小明」而非「wangxiaoming」
        """
        super().__init__(*args, **kwargs)
        # 自定義 repair_user 下拉選單顯示格式：顯示姓名而非帳號
        if 'repair_user' in self.fields:
            # lambda obj: 為每個 User 物件定義顯示文字的規則
            # obj 代表資料庫中的每一個 User 使用者物件
            self.fields['repair_user'].label_from_instance = lambda obj: (
                obj.profile.user_name if hasattr(obj, 'profile') and obj.profile.user_name 
                else obj.username
            )