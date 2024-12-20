from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import EmissionRecord

@receiver(pre_save, sender=EmissionRecord)
def set_default_pollutant(sender, instance, **kwargs):
    if not instance.pollutant:  # Якщо поле не заповнене
        instance.pollutant = "Default Pollutant"
