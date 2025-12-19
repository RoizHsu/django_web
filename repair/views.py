from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .repair import RepairForm
from .models import Repair


@login_required
def repair(request):
    repairs = Repair.objects.all()
    form = RepairForm()
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair_obj = form.save(commit=False)
            repair_obj.repair_user = request.user
            repair_obj.save()
            return redirect("/inquire")
    context = {
        'repair': form,
        'repairs': repairs
    }
    return render(request, 'repair.html', context)


@login_required
def inquire(request):
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


@login_required
def update(request, pk):
    repairs = Repair.objects.get(id=pk)
    form = RepairForm(instance=repairs)
    if request.method == 'POST':
        form = RepairForm(request.POST, instance=repairs)
        if form.is_valid():
            form.save()
            return redirect("/index")
    context = {
        'repair': form
    }
    return render(request, 'repair_update.html', context)


@login_required
def delete(request, pk):
    repairs = Repair.objects.get(id=pk)
    if request.method == 'POST':
        repairs.delete()
        return redirect("/index")
    context = {
        'repair': repairs
    }
    return render(request, 'repair_delete.html', context)