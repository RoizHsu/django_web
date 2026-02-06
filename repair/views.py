from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .repair import RepairForm
from .models import Repair


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


