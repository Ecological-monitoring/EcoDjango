from django.apps import AppConfig
# нах


class EcoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eco'

    def ready(self):
        import eco.signals  # Імпортуємо сигнали
