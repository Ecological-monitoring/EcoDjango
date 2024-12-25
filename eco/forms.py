from django import forms
from .models import EmissionRecord
from .models import TaxCalculation
from .models import RiskAssessment
from .models import DamageRecord
from .models import EmergencyEvent
from .models import PollutionRecord
from .models import Pollutant
from .models import PollutantDetails


class PollutionTaxForm(forms.Form):
    object_name = forms.CharField(max_length=100, label="Назва об'єкта")
    pollutant = forms.CharField(max_length=100, label="Забруднююча речовина", widget=forms.TextInput(attrs={
        'placeholder': 'Введіть забруднюючу речовину'
    }))
    volume = forms.FloatField(label="Об'єм викидів (тонн)", widget=forms.NumberInput(attrs={
        'placeholder': 'Введіть об\'єм у тоннах'
    }))

class PollutionRecordForm(forms.ModelForm):
    class Meta:
        model = PollutionRecord
        fields = ['company', 'year', 'value', 'substance']

class EmissionTaxForm(forms.ModelForm):
    class Meta:
        model = EmissionRecord
        fields = ['object_name', 'pollutant', 'emission_volume', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pollutant'].queryset = Pollutant.objects.all()
        print(self.fields['pollutant'].queryset)  # Друк списку записів для перевірки


class TaxCalculationForm(forms.ModelForm):
    class Meta:
        model = TaxCalculation
        fields = ['object_name', 'pollutant', 'emission_volume', 'tax_rate']

class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['object_name', 'pollutant', 'concentration']
        labels = {
            'object_name': 'Назва об\'єкта',
            'pollutant': 'Забруднююча речовина',
            'concentration': 'Концентрація речовини, мг/м³'
        }



class DamageRecordForm(forms.ModelForm):
    class Meta:
        model = DamageRecord
        fields = [
            'object_name',
            'pollutant',
            'emission_volume',
            'region_coefficient',
            'violation_characteristic',
            'year',
            'damage_type'
        ]
        widgets = {
            'object_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Назва об'єкта"}),
            'pollutant': forms.Select(attrs={'class': 'form-control'}),
            'emission_volume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Обсяг викидів'}),
            'region_coefficient': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Регіональний коефіцієнт'}),
            'violation_characteristic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Коефіцієнт порушення'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Рік'}),
            'damage_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'object_name': "Назва об'єкта",
            'pollutant': "Забруднююча речовина",
            'emission_volume': "Обсяг викидів (М)",
            'region_coefficient': "Регіональний коефіцієнт (К₃)",
            'violation_characteristic': "Коефіцієнт порушення (К₂)",
            'year': "Рік",
            'damage_type': "Тип завданої шкоди",
        }
class EmergencyEventForm(forms.ModelForm):
    class Meta:
        model = EmergencyEvent
        fields = ['name', 'event_type', 'date', 'location', 'impact']




class PollutantDetailsForm(forms.ModelForm):
    class Meta:
        model = PollutantDetails
        fields = ['name', 'hazard_class', 'mpc', 'rfc', 'sf', 'specific_emissions',  'hazard_coefficient']

class PollutantForm(forms.ModelForm):
    class Meta:
        model = Pollutant
        fields = ['name', 'description']  # Вкажіть усі необхідні поля

