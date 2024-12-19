from django.shortcuts import render, redirect, get_object_or_404
from .models import PollutionRecord
from .forms import PollutionRecordForm
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib import messages

def record_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'date')  # Сортування за замовчуванням - за датою

    # Фільтрація записів за останні 10 років
    ten_years_ago = datetime.now().date() - timedelta(days=365*10)
    records = PollutionRecord.objects.filter(date__gte=ten_years_ago)

    # Пошук
    if query:
        records = records.filter(Q(object_name__icontains=query))

    # Сортування
    if sort_by in ['object_name', 'pollutant', 'volume', 'date']:
        records = records.order_by(sort_by)

    return render(request, 'record_list.html', {'records': records, 'query': query, 'sort_by': sort_by})


def record_create(request):
    if request.method == 'POST':
        form = PollutionRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запис успішно створено!")
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
            messages.success(request, "Запис успішно оновлено!")
            return redirect('record_list')
    else:
        form = PollutionRecordForm(instance=record)
    return render(request, 'record_form.html', {'form': form})


def record_delete(request, pk):
    record = get_object_or_404(PollutionRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Запис успішно видалено!")
        return redirect('record_list')
    return render(request, 'record_confirm_delete.html', {'record': record})
