from django import forms
from .models import TitleAnnouncement
from ckeditor.widgets import CKEditorWidget

#新增表單
class TitleAnnouncementForm(forms.ModelForm):
    announcement = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = TitleAnnouncement
        fields = ['title', 'announcement', 'repair_user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'repair_user': forms.Select(attrs={'class': 'form-control'}),
        }