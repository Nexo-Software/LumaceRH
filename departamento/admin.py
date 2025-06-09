from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import DepartamentoModel


@admin.register(DepartamentoModel)
class DepartamentoAdmin(ModelAdmin, ImportExportModelAdmin):
    import_id_fields = ('id',)
    """Admin para el departamento"""
    list_display = ('nombre', 'empresa', 'encargado', 'status')
    list_editable = ('status',)
    autocomplete_fields = ('empresa', 'encargado')
    fieldsets = (
        ('Información del departamento', {
            'fields': ('nombre', 'empresa', 'encargado')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        })
    )
    search_fields = ('nombre', 'empresa__razon_social', 'encargado__username')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)