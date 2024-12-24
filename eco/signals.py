from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import EmissionRecord, Pollutant

@receiver(pre_save, sender=EmissionRecord)
def set_default_pollutant(sender, instance, **kwargs):
    # Перевіряємо, чи поле `pollutant` заповнене
    if not instance.pollutant:  # Поле `pollutant` — ForeignKey
        default_pollutant = Pollutant.objects.first()  # Беремо перший запис у таблиці Pollutant
        if default_pollutant:
            instance.pollutant = default_pollutant
        else:
            raise ValueError("Таблиця Pollutant порожня. Додайте записи до таблиці.")
