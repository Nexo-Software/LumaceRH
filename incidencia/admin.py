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
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion')
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

@admin.register(TiposFormulasModel)
class TiposFormulasAdmin(ModelAdmin):
    """Admin para los tipos de formulas"""
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('nombre',)
    list_per_page = 10
    list_editable = ('descripcion',)
    list_display_links = ('nombre',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion')
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

@admin.register(FormulaIncidenciasModel)
class FormulaIncidenciasAdmin(ModelAdmin):
    """Admin para las formulas de incidencias"""
    list_display = ('nombre', 'descripcion', 'codigo')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('nombre',)
    list_per_page = 10
    list_editable = ('descripcion', 'codigo')
    list_display_links = ('nombre',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'codigo', 'formula_detalle')
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

@admin.register(TipoIncidenciasModel)
class TipoIncidenciasAdmin(ModelAdmin):
    """Admin para los tipos de incidencias"""
    list_display = ('nombre', 'descripcion', 'categoria', 'formula')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('nombre',)
    list_per_page = 10
    list_editable = ('descripcion', 'categoria', 'formula')
    list_display_links = ('nombre',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'categoria', 'formula')
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

@admin.register(IncidenciasEmpleados)
class IncidenciasEmpleadosAdmin(ModelAdmin):
    """Admin para las incidencias de los empleados"""
    
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)