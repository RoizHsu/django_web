from django.shortcuts import render,redirect
from repair.repair import RepairForm
from repair.models import Repair

# Create your views here.


def index(request):
    repairs = Repair.objects.all()
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/repair')
    context = {
        'repairs': repairs
    }
    return render(request, 'index.html', context)




