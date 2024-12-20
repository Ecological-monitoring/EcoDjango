from django import forms
from .models import EmissionRecord
from .models import TaxCalculation

class PollutionTaxForm(forms.Form):
    object_name = forms.CharField(max_length=100, label="Назва об'єкта")
    pollutant = forms.CharField(max_length=100, label="Забруднююча речовина", widget=forms.TextInput(attrs={
        'placeholder': 'Введіть забруднюючу речовину'
    }))
    volume = forms.FloatField(label="Об'єм викидів (тонн)", widget=forms.NumberInput(attrs={
        'placeholder': 'Введіть об\'єм у тоннах'
    }))


class EmissionTaxForm(forms.ModelForm):
    class Meta:
        model = EmissionRecord
        fields = ['object_name', 'pollutant_name', 'emission_volume', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pollutant_name'].widget = forms.TextInput(attrs={
            'placeholder': 'Введіть забруднюючу речовину'
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
        fields = '__all__'