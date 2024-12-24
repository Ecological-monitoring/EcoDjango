from django.db import models

class Pollutant(models.Model):
    name = models.CharField(max_length=100, help_text="Назва забруднюючої речовини")
    description = models.TextField(blank=True, null=True, help_text="Опис забруднюючої речовини")

    class Meta:
        db_table = 'eco_pollutant'  # Назва таблиці

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


class PollutionRecord(models.Model):
    SUBSTANCE_CHOICES = [
        ('Оксид вуглецю', 'Оксид вуглецю'),
        ('Речовини у вигляді суспендованих твердих частинок', 'Речовини у вигляді суспендованих твердих частинок'),
        ('Діоксид азоту', 'Діоксид азоту'),
        ('Аміак', 'Аміак'),
        ('Сірки діоксид', 'Сірки діоксид'),
        ('Метан', 'Метан'),
    ]

    company = models.CharField(max_length=255)  # Назва компанії
    year = models.IntegerField()  # Рік
    value = models.FloatField()  # Значення викидів
    substance = models.CharField(max_length=255, choices=SUBSTANCE_CHOICES)  # Вибір речовини

    def __str__(self):
        return f"{self.company} ({self.year}) - {self.substance}"


class TaxCalculation(models.Model):
    object_name = models.CharField(max_length=255, verbose_name="Назва об'єкта")
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, verbose_name="Забруднююча речовина", default=1)
    emission_volume = models.FloatField(verbose_name="Об'єм викидів (тонн)")
    tax_rate = models.FloatField(verbose_name="Ставка податку (грн/тонна)")
    tax_sum = models.FloatField(verbose_name="Сума податку (грн)", blank=True, null=True)
    calculation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата розрахунку")

    def save(self, *args, **kwargs):
        """Автоматичне обчислення суми податку перед збереженням."""
        if self.tax_rate and self.emission_volume:
            self.tax_sum = self.tax_rate * self.emission_volume
        super().save(*args, **kwargs)

class EmissionRecord(models.Model):
    object_name = models.CharField(max_length=255, verbose_name="Назва об'єкта")
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, verbose_name="Забруднююча речовина")
    emission_volume = models.FloatField(verbose_name="Об'єм викидів (тонн)")
    date = models.DateField(verbose_name="Дата викиду")

    def __str__(self):
        return f"{self.object_name} - {self.pollutant.name} - {self.date}"

class RiskAssessment(models.Model):
    object_name = models.CharField(max_length=100, help_text="Назва об'єкта")
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, help_text="Забруднююча речовина")
    concentration = models.FloatField(help_text="Концентрація речовини, мг/м³")
    risk_level = models.CharField(max_length=100, blank=True, help_text="Рівень ризику")
    date = models.DateField(auto_now_add=True, help_text="Дата оцінки")


    def calculate_risk(self):
        """Обчислення ризику на основі методики"""
        # Додайте тут логіку оцінки ризику відповідно до методики
        if self.concentration > 1.0:  # Замініть 1.0 на ваші реальні порогові значення
            self.risk_level = "Високий"
        else:
            self.risk_level = "Низький"
        return self.risk_level

    def save(self, *args, **kwargs):
        self.calculate_risk()
        super().save(*args, **kwargs)


class DamageRecord(models.Model):
    object_name = models.CharField(max_length=255, verbose_name="Назва об'єкта")
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, verbose_name="Забруднююча речовина")
    year = models.IntegerField(verbose_name="Рік")
    damage_type = models.CharField(max_length=255, choices=[
        ('Air', 'Викиди в атмосферу'),
        ('Water', 'Скиди у водні об’єкти'),
        ('Soil', 'Забруднення ґрунту'),
    ], verbose_name="Тип завданої шкоди")
    damage_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума збитків")

    def __str__(self):
        return f"{self.object_name} ({self.year})"



class EmergencyEvent(models.Model):
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=200)
    impact = models.TextField()

    def __str__(self):
        return self.name
