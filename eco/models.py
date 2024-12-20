from django.db import models

class Pollutant(models.Model):
    name = models.CharField(max_length=100, help_text="Назва забруднюючої речовини")
    description = models.TextField(blank=True, null=True, help_text="Опис забруднюючої речовини")

    def __str__(self):
        return self.name

class TaxRate(models.Model):
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, help_text="Забруднююча речовина")
    rate = models.FloatField(help_text="Ставка податку за 1 тонну (грн)")

    def __str__(self):
        return f"{self.pollutant.name}: {self.rate} грн/тонна"

class EmissionRecord(models.Model):
    object_name = models.CharField(max_length=100, help_text="Назва об'єкта")
    pollutant = models.ForeignKey(
        Pollutant, on_delete=models.CASCADE, help_text="Забруднююча речовина"
    )  # Зміна з CharField на ForeignKey
    volume = models.FloatField(help_text="Об'єм викидів у тоннах")
    date = models.DateField(help_text="Дата викиду")

    def __str__(self):
        return f"{self.object_name} - {self.pollutant.name} - {self.date}"

    @property
    def tax(self):
        """Обчислення податку на основі ставки податку для забруднювача."""
        try:
            tax_rate = TaxRate.objects.get(pollutant=self.pollutant)
            return self.volume * tax_rate.rate
        except TaxRate.DoesNotExist:
            return 0
