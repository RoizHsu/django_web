from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 註冊後自動登入
            return redirect("home")  # 請改成你的首頁路由名稱
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
