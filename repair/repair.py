from django import forms
from django.utils import timezone

from.models import Repair,Job_title,RepairUser,Location,State


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = '__all__'
        widgets = {
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'ext': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'share': forms.TextInput(attrs={'class': 'form-control'}),
            'F': forms.NumberInput(attrs={'class': 'form-control'}),
            'offer': forms.TextInput(attrs={'class': 'form-control'}),
            'Q':forms.TextInput(attrs={'class': 'form-control'}),
            'A':forms.TextInput(attrs={'class': 'form-control'}),
            'start': forms.DateTimeInput(attrs={'type': 'datetime',}),
            'finish': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
        labels = { #顯示名稱
            'ip': 'IP',
            'ext': '分機',
            'name': '叫修人',
            'share': '股別',
            'jt': '職稱',
            'repairUser': '工程師',
            'location': '位置',
            'F': '樓層',
            'office': '科室',
            'Q': '報修問題',
            'A': '回復報修',
            'state' : '狀態',
            'start': '維修時間',
            'finish': '維修結束',
        }
