from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import PuestoModel

@admin.register(PuestoModel)
class PuestoAdmin(ModelAdmin, ImportExportModelAdmin):
    import_id_fields = ('id',)
    """Admin para el puesto"""
    list_display = ('nombre', 'departamento', 'status')
    search_fields = ('nombre', 'departamento__nombre')
    autocomplete_fields = ('departamento',)
    list_editable = ('status',)
    fieldsets = (
        ('Información del puesto', {
            'fields': ('nombre', 'departamento')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
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