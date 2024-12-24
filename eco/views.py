from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, timedelta
from .models import EmissionRecord, TaxRate, Pollutant, RiskAssessment, TaxCalculation
from .forms import EmissionTaxForm, TaxCalculationForm, RiskAssessmentForm
from .forms import DamageRecordForm
from .models import DamageRecord
from datetime import datetime
from .models import EmergencyEvent
from .forms import EmergencyEventForm
from .forms import PollutionRecord
from .models import Pollutant
from .models import PollutantDetails
from .forms import PollutantDetailsForm
import logging
def tax_results(request):
    """
    Відображає результати останнього розрахунку та історію.
    """
    results = TaxCalculation.objects.all().order_by('-calculation_date')
    latest = results.first()
    history = results[1:]
    return render(request, 'tax_results.html', {'latest': latest, 'history': history})


def calculate_tax(request):
    if request.method == 'POST':
        object_name = request.POST.get('object_name')
        pollutant_name = request.POST.get('pollutant_name')
        emission_volume = float(request.POST.get('emission_volume', 0))
        tax_rate = float(request.POST.get('tax_rate', 0))
        tax_sum = emission_volume * tax_rate

        # Збереження в базу даних
        TaxCalculation.objects.create(
            object_name=object_name,
            pollutant_name=pollutant_name,
            emission_volume=emission_volume,
            tax_rate=tax_rate,
            tax_sum=tax_sum
        )

        return redirect('tax_results')  # Перехід до сторінки з результатами

    return render(request, 'calculate_tax.html')
def add_emission_record(request):
    if request.method == 'POST':
        form = EmissionTaxForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = EmissionTaxForm()
        print(form.fields['pollutant'].queryset)  # Друк усього списку записів
    return render(request, 'add_emission_record.html', {'form': form})

def record_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'date')

    records = EmissionRecord.objects.all()

    if query:
        records = records.filter(
            Q(object_name__icontains=query) | Q(pollutant__name__icontains=query)
        )

    if sort_by in ['date', 'object_name', 'pollutant__name', 'emission_volume']:
        records = records.order_by(sort_by)

    return render(request, 'record_list.html', {'records': records, 'query': query, 'sort_by': sort_by})


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

        pollutant = get_object_or_404(Pollutant, id=pollutant_id)

        if concentration > 10:
            risk_level = "High"
        elif concentration > 5:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        RiskAssessment.objects.create(
            object_name=object_name,
            pollutant=pollutant,
            concentration=concentration,
            risk_level=risk_level
        )

        return redirect('risk_results')

    pollutants = Pollutant.objects.all()
    return render(request, 'assess_risk.html', {'pollutants': pollutants})

def risk_results(request):
    assessments = RiskAssessment.objects.all()
    return render(request, 'risk_results.html', {'assessments': assessments})

def calculate_risk(concentration):
    """Розрахунок ризику залежно від концентрації."""
    if concentration < 0.05:
        return "Низький"
    elif 0.05 <= concentration < 0.1:
        return "Середній"
    else:
        return "Високий"

def damage_list(request):
    records = DamageRecord.objects.all()
    return render(request, 'damage_list.html', {'records': records})

def add_damage_record(request):
    if request.method == 'POST':
        form = DamageRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('damage_list')
    else:
        form = DamageRecordForm()
    return render(request, 'add_damage_record.html', {'form': form})
def damage_records(request):
    """Відображення сторінки введення даних про збитки."""
    pollutants = Pollutant.objects.all()
    current_year = datetime.now().year
    return render(request, 'damage_records.html', {'pollutants': pollutants, 'current_year': current_year})

def calculate_damage(request):
    """Обробка форми і збереження даних про збитки."""
    if request.method == 'POST':
        form = DamageRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('damage_results')
    else:
        form = DamageRecordForm()
    return render(request, 'damage_records.html', {'form': form})

def damage_results(request):
    """Відображення результатів розрахунків збитків."""
    results = DamageRecord.objects.all()
    return render(request, 'damage_results.html', {'results': results})



def home(request):
    return render(request, 'record_list.html')

def add_event(request):
    if request.method == 'POST':
        form = EmergencyEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_results')
    else:
        form = EmergencyEventForm()
    return render(request, 'add_damage_record.html', {'form': form})

def view_results(request):
    events = EmergencyEvent.objects.all()
    return render(request, 'damage_results.html', {'events': events})

def pollutant_table(request):
    pollutants = PollutantDetails.objects.all()
    return render(request, 'pollutant_table.html', {'pollutants': pollutants})

def delete_pollutant(request, pk):
    pollutant = get_object_or_404(PollutantDetails, pk=pk)
    pollutant.delete()
    return redirect('pollutant_table')

def pollutant_add(request):
    if request.method == 'POST':
        form = PollutantDetailsForm(request.POST)
        if form.is_valid():
            form.save()  # Автоматично обчислить tax_rate та kn
            return redirect('pollutant_table')  # Повертаємось до таблиці
    else:
        form = PollutantDetailsForm()
    return render(request, 'pollutant_add.html', {'form': form})