
# нах
# Register your models here.
from django.contrib import admin
from .models import TaxCalculation
from .models import TaxRate, EmissionRecord

@admin.register(TaxCalculation)
class TaxCalculationAdmin(admin.ModelAdmin):
    list_display = ('object_name', 'pollutant_name', 'tax_type', 'calculation_date', 'tax_sum')
    list_filter = ('tax_type', 'calculation_date')
    search_fields = ('object_name', 'pollutant_name')
@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = ['object_name', 'get_pollutant_name', 'emission_volume', 'date']

    def get_pollutant_name(self, obj):
        return obj.pollutant.name
    get_pollutant_name.short_description = 'Назва забруднювача'
