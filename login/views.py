from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from login.login import LoginForm
from django.contrib import auth

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/index/')
        #帳號密碼錯誤跳出提示
        else:
            error_message = '帳號或密碼輸入錯誤，請重新輸入'
    
    return render(request, 'login.html', {'error_message': error_message})


# 登出
def logout(request):

    auth.logout(request)
    return HttpResponseRedirect('/login') #重新導向到登入畫面
