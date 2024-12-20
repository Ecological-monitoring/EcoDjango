from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import EmissionRecord

@receiver(pre_save, sender=EmissionRecord)
def set_default_pollutant(sender, instance, **kwargs):
    # Перевіряємо, чи поле `pollutant_name` заповнене
    if not instance.pollutant_name:  # Використовуємо правильну назву поля
        instance.pollutant_name = "Default Pollutant"
