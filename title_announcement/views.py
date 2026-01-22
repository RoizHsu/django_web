from django.shortcuts import render, redirect
from .models import TitleAnnouncement
from .forms import TitleAnnouncementForm
from django.contrib import messages #訊息閃示
from django.shortcuts import get_object_or_404 #導入get_object_or_404函數
from django.contrib.auth.decorators import login_required#鎖沒有登入會跳轉到登入頁面
from django.http import HttpResponseForbidden #用來回傳Http 404 錯誤狀態碼的工具

import math #導入math模組 使用math.ceil()函數
# Create your views here.

page = 1  #當前頁數
def index(request):
    announcements = TitleAnnouncement.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'title_announcements': announcements})

#@login_required #鎖沒有登入會跳轉到登入頁面 #公告編輯頁 #這個跟下方code會衝突所以先註解掉
def editor(request):# 檢查使用者是否有權限（is_staff工作人員狀態 或特定群組）
    if not request.user.is_staff:
        messages.error(request, '您沒有權限訪問此頁面，請聯絡管理員申請權限。')
        return redirect('index')  # 重定向到首頁
    
    if request.method == 'POST':
        form = TitleAnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            # 如果需要設置當前登入用戶為發布人
            if request.user.is_authenticated:
                announcement.repair_user = request.user
            announcement.save()
            return redirect('index')  # 儲存後重新導向
        else:
            # 表單驗證失敗，返回錯誤
            print("表單錯誤:", form.errors)
    else:
        form = TitleAnnouncementForm()
    return render(request, 'editor.html', {'form': form})
# 取得單一公告物件，若找不到則回報 404 錯誤
def  announcement_detail(request, announcement_id):
    post = get_object_or_404(TitleAnnouncement, id=announcement_id)
    return render(request, 'announcement_detail.html', {'announcement': post})