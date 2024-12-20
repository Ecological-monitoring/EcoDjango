from django import forms

from .models import EmissionRecord


class PollutionTaxForm(forms.Form):
    object_name = forms.CharField(max_length=100, label="Назва об'єкта")
    pollutant = forms.CharField(max_length=100, label="Забруднююча речовина")
    volume = forms.FloatField(label="Об'єм викидів (тонн)")

class EmissionTaxForm(forms.ModelForm):
    class Meta:
        model = EmissionRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Значення за замовчуванням
        self.fields['pollutant'].initial = "Default Pollutant"