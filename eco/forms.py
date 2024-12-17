from django import forms
from .models import PollutionRecord

class PollutionRecordForm(forms.ModelForm):
    class Meta:
        model = PollutionRecord
        fields = ['object_name', 'pollutant', 'volume']
