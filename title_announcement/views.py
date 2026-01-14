from django.shortcuts import render, redirect
from .models import TitleAnnouncement
from .forms import TitleAnnouncementForm
import math #導入math模組 使用math.ceil()函數
# Create your views here.

page = 1  #當前頁數
def new_index(request):
    announcements = TitleAnnouncement.objects.all().order_by('-created_at')
    return render(request, 'new_index.html', {'title_announcements': announcements})

def editor(request):
    if request.method == 'POST':
        form = TitleAnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            # 如果需要設置當前登入用戶為發布人
            if request.user.is_authenticated:
                announcement.repair_user = request.user
            announcement.save()
            return redirect('new_index')  # 儲存後重新導向
        else:
            # 表單驗證失敗，返回錯誤
            print("表單錯誤:", form.errors)
    else:
        form = TitleAnnouncementForm()
    return render(request, 'editor.html', {'form': form})
