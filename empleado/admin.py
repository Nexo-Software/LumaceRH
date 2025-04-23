from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.
from .models import EmpleadoModel, PostulanteModel

@admin.register(PostulanteModel)
class PostulanteAdmin(ModelAdmin):
    list_display = ('usuario__first_name', 'puesto', 'contrato', 'direccion', 'estado')
    autocomplete_fields = ('usuario', 'puesto', 'contrato')
    search_fields = ('usuario__username', 'puesto', 'contrato')
    list_filter = ('estado',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    fieldsets = (
        ('Información del postulante', {
            'fields': ('usuario', 'puesto', 'contrato', 'notas')
        }),
        ('Dirección', {
            'fields': ('calle', 'numero', 'ciudad', 'codigo_postal', 'provincia', 'pais')
        }),
        ('Estado del postulante', {
            'fields': ('estado',)
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        })
    )
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        
@admin.register(EmpleadoModel)
class EmpleadoAdmin(ModelAdmin):
    list_display = ('postulante', 'puesto', 'contrato', 'sucursal', 'status')
    list_editable = ('status',)
    search_fields = ('postulante__usuario__username', 'puesto', 'contrato')
    autocomplete_fields = ('postulante', 'puesto', 'contrato', 'sucursal')
    fieldsets = (
        ('Información del empleado', {
            'fields': ('postulante', 'puesto', 'contrato', 'sucursal', 'notas')
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