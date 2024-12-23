from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, timedelta
from .models import EmissionRecord, TaxRate, Pollutant
from .forms import EmissionTaxForm
from django.core.exceptions import ValidationError
from .forms import TaxCalculationForm
# Функція для розрахунку податку
from .models import TaxCalculation
from django.shortcuts import render
from .models import RiskAssessment
from .forms import RiskAssessmentForm
def tax_results(request):
    """
    Відображає результати останнього розрахунку та історію.
    """
    results = TaxCalculation.objects.all().order_by('-calculation_date')  # Усі розрахунки
    latest = results.first()  # Останній розрахунок
    history = results[1:]  # Уся історія без останнього запису
    return render(request, 'tax_results.html', {'latest': latest, 'history': history})
# Функція для розрахунку податку
def calculate_tax(request):
    if request.method == 'POST':
        form = TaxCalculationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tax_results')  # Перенаправлення на сторінку результатів
    else:
        form = TaxCalculationForm()
    return render(request, 'calculate_tax.html', {'form': form})
# Функція для додавання запису про викиди
def add_emission_record(request):
    if request.method == 'POST':
        form = EmissionTaxForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            if not record.pollutant_name:  # Якщо поле пусте
                record.pollutant_name = "Default Pollutant"
            record.save()
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
    records = EmissionRecord.objects.filter(date__gte=ten_years_ago)

    # Пошук
    if query:
        records = records.filter(Q(object_name__icontains=query))

    # Сортування
    if sort_by in ['object_name', 'pollutant_name', 'emission_volume', 'date']:
        records = records.order_by(sort_by)

    return render(request, 'record_list.html', {'records': records, 'query': query, 'sort_by': sort_by})


# Створення запису
def record_create(request):
    if request.method == 'POST':
        form = EmissionTaxForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запис успішно створено!")
            return redirect('record_list')
    else:
        form = EmissionTaxForm()
    return render(request, 'record_form.html', {'form': form})


# Редагування запису
def record_edit(request, pk):
    record = get_object_or_404(EmissionRecord, pk=pk)
    if request.method == 'POST':
        form = EmissionTaxForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Запис успішно оновлено!")
            return redirect('record_list')
    else:
        form = EmissionTaxForm(instance=record)
    return render(request, 'record_form.html', {'form': form})


# Видалення запису
def record_delete(request, pk):
    record = get_object_or_404(EmissionRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Запис успішно видалено!")
        return redirect('record_list')
    return render(request, 'record_confirm_delete.html', {'record': record})


def assess_risk(request):
    if request.method == 'POST':
        object_name = request.POST.get('object_name')
        pollutant_id = request.POST.get('pollutant')
        concentration = float(request.POST.get('concentration'))

        pollutant = Pollutant.objects.get(id=pollutant_id)

        # Логіка для оцінки ризику
        if concentration > 10:  # Приклад розрахунку рівня ризику
            risk_level = "High"
        elif concentration > 5:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        assessment = RiskAssessment.objects.create(
            object_name=object_name,
            pollutant=pollutant,
            concentration=concentration,
            risk_level=risk_level
        )

        return redirect('risk_results')

    pollutants = Pollutant.objects.all()
    return render(request, 'assess_risk.html', {'pollutants': pollutants})


def risk_results(request):
    results = RiskAssessment.objects.all()
    return render(request, 'risk_results.html', {'results': results})

def calculate_risk_level(concentration):
    assessments = RiskAssessment.objects.all()
    return render(request, 'risk_results.html', {'assessments': assessments})

