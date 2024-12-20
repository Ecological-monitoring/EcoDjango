from django.db import models

class Pollutant(models.Model):
    name = models.CharField(max_length=100, help_text="Назва забруднюючої речовини")
    description = models.TextField(blank=True, null=True, help_text="Опис забруднюючої речовини")

    def __str__(self):
        return self.name


class TaxRate(models.Model):
    pollutant = models.CharField(max_length=255, verbose_name="Забруднююча речовина")
    rate = models.FloatField(verbose_name="Ставка податку (грн за тонну)")

    def __str__(self):
        return f"{self.pollutant}: {self.rate} грн/тонна"

    @property
    def tax(self):
        """Обчислення податку на основі ставки податку для забруднювача."""
        try:
            tax_rate = TaxRate.objects.get(pollutant__name=self.pollutant_name)
            return self.emission_volume * tax_rate.rate
        except TaxRate.DoesNotExist:
            return 0  # Якщо ставка податку не знайдена, податок дорівнює 0



class TaxCalculation(models.Model):
    TAX_TYPES = [
        ('air_emissions', 'Викиди в атмосферу'),
        ('water_discharge', 'Скиди у водні об’єкти'),
        ('waste_disposal', 'Розміщення відходів'),
        ('radioactive_waste', 'Утворення радіоактивних відходів'),
        ('temporary_storage', 'Тимчасове зберігання радіоактивних відходів'),
    ]

    object_name = models.CharField(max_length=255, verbose_name="Назва об'єкта")
    pollutant_name = models.CharField(max_length=255, verbose_name="Назва забруднюючої речовини")
    emission_volume = models.FloatField(verbose_name="Об'єм викидів", default=0)
    tax_rate = models.FloatField(verbose_name="Ставка податку")
    tax_sum = models.FloatField(verbose_name="Сума податку", blank=True, null=True)
    tax_type = models.CharField(max_length=50, choices=TAX_TYPES, verbose_name="Тип податку")
    calculation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата розрахунку")

    def save(self, *args, **kwargs):
        """Автоматичне обчислення суми податку перед збереженням."""
        if self.tax_rate and self.emission_volume:
            self.tax_sum = self.tax_rate * self.emission_volume
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.object_name} - {self.pollutant_name} ({self.tax_type})"

class EmissionRecord(models.Model):
    """
    Модель для збереження інформації про викиди забруднюючих речовин.
    """
    object_name = models.CharField(max_length=255, verbose_name="Назва об'єкта")
    pollutant_name = models.CharField(max_length=255, verbose_name="Забруднююча речовина")
    emission_volume = models.FloatField(verbose_name="Об'єм викидів (тонн)")
    date = models.DateField(verbose_name="Дата викиду")

    def __str__(self):
        return f"{self.object_name} - {self.pollutant_name} - {self.date}"
