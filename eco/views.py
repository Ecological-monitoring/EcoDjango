from django.shortcuts import render

# Create your views here.
# Тут логіка основна
from django.shortcuts import render, redirect, get_object_or_404
from .models import PollutionRecord
from .forms import PollutionRecordForm
from datetime import datetime, timedelta

def record_list(request):
    ten_years_ago = datetime.now().date() - timedelta(days=365*10)
    records = PollutionRecord.objects.filter(date__gte=ten_years_ago)
    return render(request, 'record_list.html', {'records': records})

def record_create(request):
    if request.method == 'POST':
        form = PollutionRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = PollutionRecordForm()
    return render(request, 'record_form.html', {'form': form})

def record_edit(request, pk):
    record = get_object_or_404(PollutionRecord, pk=pk)
    if request.method == 'POST':
        form = PollutionRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = PollutionRecordForm(instance=record)
    return render(request, 'record_form.html', {'form': form})

def record_delete(request, pk):
    record = get_object_or_404(PollutionRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('record_list')
    return render(request, 'record_confirm_delete.html', {'record': record})
