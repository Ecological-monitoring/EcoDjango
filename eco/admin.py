
# нах
# Register your models here.
from django.contrib import admin
from .models import TaxCalculation
from .models import TaxRate, EmissionRecord
from .models import PollutionRecord

@admin.register(PollutionRecord)
class PollutionRecordAdmin(admin.ModelAdmin):
    list_display = ('company', 'year', 'value', 'substance')
@admin.register(TaxCalculation)
class TaxCalculationAdmin(admin.ModelAdmin):
    list_display = ('object_name', 'pollutant_name', 'emission_volume', 'tax_rate', 'tax_sum', 'calculation_date')
    search_fields = ('object_name', 'pollutant_name')
    list_filter = ('calculation_date',)
@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = ['object_name', 'get_pollutant_name', 'emission_volume', 'date']

    def get_pollutant_name(self, obj):
        return obj.pollutant.name
    get_pollutant_name.short_description = 'Назва забруднювача'
