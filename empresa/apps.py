from django.apps import AppConfig


class EmpresaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'empresa'
    def ready(self):
        # Importar señales aquí para evitar problemas de importación circular
        import empresa.signal
