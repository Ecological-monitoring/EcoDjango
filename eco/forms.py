from django import forms
from .models import EmissionRecord
from .models import TaxCalculation
from .models import RiskAssessment
from .models import DamageRecord
from .models import EmergencyEvent
from .models import PollutionRecord

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
        self.fields['pollutant'].widget = forms.Select(attrs={
            'placeholder': 'Оберіть забруднюючу речовину'
        })
        self.fields['object_name'].widget = forms.TextInput(attrs={
            'placeholder': 'Введіть назву об\'єкта'
        })
        self.fields['emission_volume'].widget = forms.NumberInput(attrs={
            'placeholder': 'Введіть об\'єм у тоннах'
        })
        self.fields['date'].widget = forms.DateInput(attrs={
            'placeholder': 'Введіть дату (рррр-мм-дд)',
            'type': 'date'
        })


class TaxCalculationForm(forms.ModelForm):
    class Meta:
        model = TaxCalculation
        fields = ['object_name', 'pollutant_name', 'emission_volume', 'tax_rate']
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
        fields = ['object_name', 'pollutant', 'year', 'damage_type', 'damage_amount']
        labels = {
            'object_name': "Назва об'єкта",
            'pollutant': "Забруднююча речовина",
            'year': "Рік",
            'damage_type': "Тип завданої шкоди",
            'damage_amount': "Сума збитків (грн)"
        }
        widgets = {
            'damage_type': forms.Select(choices=[
                ('Air', 'Викиди в атмосферу'),
                ('Water', 'Скиди у водні об’єкти')
            ])
        }

class EmergencyEventForm(forms.ModelForm):
    class Meta:
        model = EmergencyEvent
        fields = ['name', 'event_type', 'date', 'location', 'impact']


