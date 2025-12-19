from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm

@csrf_protect
def register(request):
    error_message = ''
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  # 這裡會同時建立 User 和 UserProfile
                messages.success(request, "註冊成功！請先登入。")
                return redirect("login")  # 註冊後跳轉到登入頁
            except IntegrityError as e:
                # 捕獲資料庫完整性約束錯誤
                if 'username' in str(e):
                    error_message = '此帳號已存在，請使用其他帳號。'
                elif 'email' in str(e):
                    error_message = '此電子郵件已被註冊，請使用其他電子郵件。'
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