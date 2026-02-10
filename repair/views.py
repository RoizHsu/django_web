from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .repair import RepairForm
from .models import Repair
from userMaterial.models import UserMaterial
from django.http import JsonResponse


def repair(request):
    # 檢查使用者是否已登入
    if not request.user.is_authenticated:
        messages.error(request, '請先登入才能訪問此頁面。')
        return redirect('index')  # 重定向到登入頁
    
    # 檢查使用者是否有權限（is_staff工作人員狀態 或特定群組）
    if not (request.user.is_staff or request.user.groups.filter(name='工程師').exists()):
        messages.error(request, '您沒有權限訪問此頁面，請聯絡管理員申請權限。')
        return redirect('index')  # 重定向到首頁
    
    repairs = Repair.objects.all()
    form = RepairForm()
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair_obj = form.save(commit=False)
            repair_obj.repair_user = request.user
            repair_obj.save()
            return redirect("/index")
    context = {
        'repair': form,
        'repairs': repairs
    }
    return render(request, 'repair.html', context)


#@login_required #鎖沒有登入會跳轉到登入頁面 #改用下面的方式檢查登入和權限 #不然會衝突
def inquire(request):
        # 檢查使用者是否已登入
    if not request.user.is_authenticated:
        messages.error(request, '請先登入才能訪問此頁面。')
        return redirect('index')  # 重定向到登入頁
    
    # 檢查使用者是否有權限（is_staff工作人員狀態 或特定群組）
    if not (request.user.is_staff or request.user.groups.filter(name='工程師').exists()):
        messages.error(request, '您沒有權限訪問此頁面，請聯絡管理員申請權限。')
        return redirect('index')  # 重定向到首頁
    
    inquires = Repair.objects.all()
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair_obj = form.save(commit=False)
            repair_obj.repair_user = request.user
            repair_obj.save()
            return redirect("/repair")
    context = {
        'inquires': inquires
    }
    return render(request, 'Inquire.html', context)


@login_required #鎖沒有登入會跳轉到登入頁面
def update(request, pk):
    repairs = Repair.objects.get(id=pk)
    form = RepairForm(instance=repairs)
    if request.method == 'POST':
        form = RepairForm(request.POST, instance=repairs)
        if form.is_valid():
            form.save()
            return redirect("/repair")
    context = {
        'repair': form
    }
    return render(request, 'repair_update.html', context)


@login_required #鎖沒有登入會跳轉到登入頁面
def delete(request, pk):
    repairs = Repair.objects.get(id=pk)
    if request.method == 'POST':
        repairs.delete()
        return redirect("/old_index")
    context = {
        'repair': repairs
    }
    return render(request, 'repair_delete.html', context)

def get_userMaterial_data(request):
    # 從網址獲取參數，例如 /api/get_userMaterial/?ext=1244
    ext_number = request.GET.get('ext', None)
    ip_number = request.GET.get('ip', None)
    #預設失敗，如果找到資料再改成成功，這樣前端就可以根據 success 來判斷是否有找到資料
    results = {'success': False, 'name': '', 'department': '', 'ip': ''}
    user_Material = None

    if ip_number:
        user_Material = UserMaterial.objects.filter(ip=ip_number).first()
    elif ext_number:
        user_Material = UserMaterial.objects.filter(ext=ext_number).first()
    if user_Material:
        results={
            'success': True,
            'name': user_Material.name,
            'ext': user_Material.ext,
            'office': user_Material.office,
            'share': user_Material.share,
            'ip': user_Material.ip,
            }
    # 回傳 JSON 格式 Vue 的 fetch 會收到的東西
    return JsonResponse(results)


