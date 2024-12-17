from django.shortcuts import render

# Create your views here.
# Тут логіка основна
from django.shortcuts import render, redirect
from .models import PollutionRecord
from .forms import PollutionRecordForm

def record_list(request):
    records = PollutionRecord.objects.all()
    return render(request, 'record_list.html', {'records': records})

def record_create(request):
    if request.method == "POST":
        form = PollutionRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = PollutionRecordForm()
    return render(request, 'record_form.html', {'form': form})
