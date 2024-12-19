from django import forms
from .models import PollutionRecord
from .models import EmissionRecord

class PollutionRecordForm(forms.ModelForm):
    class Meta:
        model = PollutionRecord
        fields = ['object_name', 'pollutant', 'volume']

class PollutionTaxForm(forms.Form):
    object_name = forms.CharField(max_length=100, label="Назва об'єкта")
    pollutant = forms.CharField(max_length=100, label="Забруднююча речовина")
    volume = forms.FloatField(label="Об'єм викидів (тонн)")

class EmissionTaxForm(forms.ModelForm):
    class Meta:
        model = EmissionRecord
        fields = ['object_name', 'pollutant', 'volume', 'date']