from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import SucursalModel

@admin.register(SucursalModel)
class SucursalAdmin(ModelAdmin):
    """Admin para la sucursal"""
    list_display = ('empresa', 'nombre', 'direccion', 'telefono', 'email', 'status')
    list_editable = ('status',)
    search_fields = ('nombre', 'empresa__razon_social',)
    autocomplete_fields = ('empresa','encargado')
    fieldsets = (
        ('Información de la sucursal', {
            'fields': ('empresa', 'nombre', 'encargado')
        }),
        ('Dirección', {
            'fields': ('calle', 'numero', 'ciudad', 'codigo_postal', 'provincia', 'pais')
        }),
        ('Datos de contacto', {
            'fields': ('telefono', 'fax', 'email', 'web')
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