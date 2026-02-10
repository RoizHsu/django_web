from django import forms
from django.utils import timezone
from .models import Repair, Job_title, Location, State


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = '__all__'
        widgets = {
            'ip': forms.TextInput(attrs={'class': 'form-control', 'v-model': 'user_material.ip', '@change': "fetchEmployeeData('ip')"}),
            'ext': forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'user_material.ext', '@change': "fetchEmployeeData('ext')"}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'v-model': 'user_material.name'}),
            'share': forms.TextInput(attrs={'class': 'form-control', 'v-model': 'user_material.share'}),
            'F': forms.NumberInput(attrs={'class': 'form-control'}),
            'office': forms.TextInput(attrs={'class': 'form-control', 'v-model': 'user_material.office'}),
            'Q': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            #rows: 4高度（4 行）cols: 40寬度（約 40 個字元）
            'A': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
             #rows: 4高度（4 行）cols: 40寬度（約 40 個字元）
            'repair_user': forms.HiddenInput(),
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'},format='%Y-%m-%dT%H:%M'),
            'finish': forms.DateTimeInput(attrs={'type': 'datetime-local'},format='%Y-%m-%dT%H:%M')
        }
        labels = {
            'ip': 'IP',
            'ext': '分機',
            'name': '叫修人',
            'share': '股別',
            'jt': '職稱',
            'repair_user': '維修工程師',
            'location': '位置',
            'F': '樓層',
            'office': '科室',
            'Q': '報修問題',
            'A': '回復報修',
            'state': '狀態',
            'start': '維修時間',
            'finish': '維修結束',
        }
