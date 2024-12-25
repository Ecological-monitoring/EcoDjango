
# нах
# Register your models here.
from django.contrib import admin
from .models import TaxCalculation
from .models import TaxRate, EmissionRecord
from .models import PollutionRecord
from .models import Pollutant
from .models import DamageRecord


admin.site.register(Pollutant)
@admin.register(PollutionRecord)
class PollutionRecordAdmin(admin.ModelAdmin):
    list_display = ('company', 'year', 'value', 'substance')
@admin.register(TaxCalculation)
class TaxCalculationAdmin(admin.ModelAdmin):
    list_display = ('object_name', 'get_pollutant_name', 'emission_volume', 'tax_rate', 'tax_sum', 'calculation_date')
    search_fields = ('object_name',)
    list_filter = ('calculation_date',)

    def get_pollutant_name(self, obj):
        return obj.pollutant_name if hasattr(obj, 'pollutant_name') else 'N/A'
    get_pollutant_name.short_description = 'Назва забруднювача'

@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = ['object_name', 'get_pollutant_name', 'emission_volume', 'date']

    def get_pollutant_name(self, obj):
        return obj.pollutant.name if obj.pollutant else 'N/A'
    get_pollutant_name.short_description = 'Назва забруднювача'

@admin.register(DamageRecord)
class DamageRecordAdmin(admin.ModelAdmin):
    list_display = ('object_name', 'pollutant', 'emission_volume', 'damage_type', 'year', 'damage_amount')
    search_fields = ('object_name', 'pollutant__name', 'year')
    list_filter = ('damage_type', 'year')