from django.shortcuts import render, redirect
from .models import TitleAnnouncement
from .forms import TitleAnnouncementForm
from django.shortcuts import get_object_or_404 #導入get_object_or_404函數
from django.contrib.auth.decorators import login_required
import math #導入math模組 使用math.ceil()函數
# Create your views here.

page = 1  #當前頁數
def index(request):
    announcements = TitleAnnouncement.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'title_announcements': announcements})
@login_required #鎖沒有登入會跳轉到登入頁面 #公告編輯頁
def editor(request):
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