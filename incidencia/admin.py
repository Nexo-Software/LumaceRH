from unfold.admin import ModelAdmin, TabularInline
from django.contrib import admin
# Modelos
from .models import CategoriaIncidenciasModel, TiposFormulasModel, FormulaIncidenciasModel, TipoIncidenciasModel, IncidenciasEmpleados

@admin.register(CategoriaIncidenciasModel)
class CategoriaIncidenciasAdmin(ModelAdmin):
    """Admin para la categoria de incidencias"""
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('nombre',)
    list_per_page = 10
    list_editable = ('descripcion',)
    list_display_links = ('nombre',)
    