from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # 這裡會同時建立 User 和 UserProfile
            messages.success(request, "註冊成功！請先登入。")
            return redirect("login")  # 註冊後跳轉到登入頁
        else:
            messages.error(request, "註冊失敗，請檢查輸入。")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})