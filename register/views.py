from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm
from django.db import transaction
from django.http import JsonResponse
from .models import Calendar_Shift, UserProfile
from django.contrib.auth.models import User

@csrf_protect
def register(request):
    error_message = ''
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()  # 這裡會同時建立 User 和 UserProfile   # 使用原子交易確保資料一致性
                    login(request, user)  # 註冊後自動登入
                    return redirect("login")  # 註冊後跳轉到登入頁
            except IntegrityError as e:
                # 捕獲資料庫完整性約束錯誤
                if 'username' in str(e):
                    error_message = '此帳號已存在，請使用其他帳號。'
                elif 'email' in str(e):
                    error_message = '此電子郵件已被註冊，請使用其他電子郵件。'
                elif 'identity' in str(e):
                    error_message = '此身份證字號已被註冊，請確認身份證字號。'
                elif 'phone' in str(e):
                    error_message = '此電話號碼已被註冊，請使用其他電話號碼。'
                else:
                    error_message = '註冊失敗，請檢查輸入資料。'
        else:
            # 收集所有表單驗證錯誤信息
            error_list = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_list.append(str(error))
            error_message = ' '.join(error_list)
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form, "error_message": error_message})


def calendar_shifts_api(request):
    """提供日曆班次數據的 API"""
    try:
        # 獲取所有用戶及其班次
        users = User.objects.filter(calendars__isnull=False).distinct()
        
        employees_data = []
        for user in users:
            # 獲取用戶姓名
            user_name = user.username
            if hasattr(user, 'profile') and user.profile.user_name:
                user_name = user.profile.user_name
            
            # 獲取該用戶的所有班次
            shifts = Calendar_Shift.objects.filter(user=user).order_by('start_time')
            
            shifts_data = []
            for shift in shifts:
                # 提取開始和結束的小時數
                start_hour = shift.start_time.hour
                end_hour = shift.end_time.hour
                
                # 如果結束時間是 0:00，設為 24（代表當天結束）
                if end_hour == 0 and shift.end_time.date() > shift.start_time.date():
                    end_hour = 24
                
                shifts_data.append({
                    'id': shift.id,
                    'title': shift.title,
                    'description': shift.description or '',
                    'start_hour': start_hour,
                    'end_hour': end_hour,
                    'start_time': shift.start_time.strftime('%Y-%m-%d %H:%M'),
                    'end_time': shift.end_time.strftime('%Y-%m-%d %H:%M'),
                })
            
            employees_data.append({
                'id': user.id,
                'name': user_name,
                'shifts': shifts_data
            })
        
        return JsonResponse({
            'success': True,
            'employees': employees_data
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)