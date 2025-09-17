from django.shortcuts import render,redirect
from .repair import RepairForm
from .models import Repair



def repair(request):
    repairs = Repair.objects.all()#查詢資料
    form = RepairForm()
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/inquire")#redirect跳轉
    context = {
        'repair': form,
        'repairs': repairs
    }
    return render(request, 'repair.html', context)


def inquire(request):
    inquires = Repair.objects.all()
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/repair")
    context = {
        'inquires': inquires

    }
    return render(request, 'Inquire.html',context)


def update(request,pk):
    repairs = Repair.objects.get(id=pk)
    form = RepairForm(instance=repairs)
    if request.method == 'POST':
        form = RepairForm(request.POST, instance=repairs)
        if form.is_valid():
            form.save()
        return redirect("/index")
    context = {
        'repair':form
    }
    return render(request, 'repair_update.html',context)


def delete(request,pk):
    repairs = Repair.objects.get(id=pk)
    if request.method == 'POST':
        repairs.delete()
        return redirect("/index")

    context = {
        'repair':repairs
    }

    return render(request, 'repair_delete.html',context)