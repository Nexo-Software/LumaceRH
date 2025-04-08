from django.contrib import admin
from .models import Postulante

@admin.register(Postulante)
class PostulanteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'puesto', 'contrato', 'notas')
    search_fields = ('usuario__username', 'puesto__nombre', 'contrato__tipo')
    list_filter = ('puesto', 'contrato')
