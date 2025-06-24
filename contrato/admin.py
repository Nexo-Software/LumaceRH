from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.

from .models import ContratoModel

@admin.register(ContratoModel)
class ContratoAdmin(ImportExportModelAdmin):
    import_id_fields = ('id',)
    """Admin para el contrato"""
    list_display = ('nombre', 'tipo_contrato', 'horas_trabajo', 'salario_base', 'fecha_inicio', 'fecha_fin', 'status')
    list_editable = ('status',)
    list_filter = ('tipo_contrato', 'status') 
    date_hierarchy = 'fecha_inicio'
    search_fields = ('nombre', 'tipo_contrato')
    fieldsets = (
        ('Información del contrato', {
            'fields': ('nombre', 'tipo_contrato', 'horas_trabajo', 'salario_base', 'fecha_inicio', 'fecha_fin')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by', 'status'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)