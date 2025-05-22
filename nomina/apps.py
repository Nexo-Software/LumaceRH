from django.apps import AppConfig


class NominaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nomina'
    def ready(self):
        import nomina.signals
