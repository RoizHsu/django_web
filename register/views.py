from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    error_message = ''
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # 這裡會同時建立 User 和 UserProfile
            messages.success(request, "註冊成功！請先登入。")
            return redirect("login")  # 註冊後跳轉到登入頁
        else:
            # 收集所有錯誤信息
            error_list = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_list.append(error)
            error_message = ' '.join(error_list)
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form, "error_message": error_message})