from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, timedelta

from .models import EmissionRecord, TaxRate, PollutionRecord
from .forms import EmissionTaxForm, PollutionRecordForm

# Функція для розрахунку податку
def calculate_tax(request):
    records = EmissionRecord.objects.all()
    total_tax = sum(record.tax for record in records)  # Сумарний податок для всіх записів
    return render(request, 'calculate_tax.html', {'records': records, 'total_tax': total_tax})

# Функція для додавання запису про викиди
def add_emission_record(request):
    if request.method == 'POST':
        form = EmissionTaxForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запис успішно створено!")
            return redirect('calculate_tax')
    else:
        form = EmissionTaxForm()
    return render(request, 'add_emission_record.html', {'form': form})

# Відображення списку записів
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

# Створення запису
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

# Редагування запису
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

# Видалення запису
def record_delete(request, pk):
    record = get_object_or_404(PollutionRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Запис успішно видалено!")
        return redirect('record_list')
    return render(request, 'record_confirm_delete.html', {'record': record})
