from django.contrib import admin

from django.utils.html import format_html
# Modelos
from .models import CategoriaIncidenciasModel, TipoIncidenciasModel, IncidenciasEmpleados, ConfiguracionIncidenciasModel
from import_export.admin import ImportExportModelAdmin

@admin.register(CategoriaIncidenciasModel)
class CategoriaIncidenciasAdmin(ImportExportModelAdmin):
    import_id_fields = ('id',)
    """Admin para la categoria de incidencias"""
    list_display = ('nombre', 'descripcion', 'codigo', 'efecto', 'status')
    search_fields = ('nombre',)
    list_editable = ('status',)
    list_filter = ('nombre',)
    ordering = ('nombre',)
    list_per_page = 10
    list_display_links = ('nombre',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion',)
        }),
        ('Detalles', {
            'fields': ('codigo', 'efecto'),
            'classes': ('collapse',)
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
class TipoIncidenciasAdmin(ImportExportModelAdmin):
    import_id_fields = ('id',)
    """Admin para los tipos de incidencias"""
    list_display = ('nombre', 'descripcion', 'categoria',)
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('nombre',)
    list_per_page = 10
    autocomplete_fields = ('categoria',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'categoria',)
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
class IncidenciasEmpleadosAdmin(ImportExportModelAdmin):
    import_id_fields = ('id',)
    """Admin para las incidencias de los empleados"""
    def get_estado_display(self, obj):
        estados = {
            'PENDIENTE': ('Pendiente', '#FFA500', '#fff'),  # Naranja para pendiente
            'APROBADA': ('Aceptado', '#4CAF50', '#fff'),   # Verde para aceptado
            'RECHAZADA': ('Rechazado', '#F44336', '#fff'),  # Rojo para rechazado
        }
        
        label, bg_color, text_color = estados.get(obj.estado_incidencia, ('Desconocido', '#999', '#fff'))
        
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 5px 10px; '
            'border-radius: 10px; font-weight: bold; font-size: 0.9em;">{}</span>',
            bg_color, text_color, label
        )
    
    get_estado_display.short_description = 'Estado'
        
    list_display = ('empleado', 'tipo_incidencia', 'fecha', 'get_estado_display', 'monto', 'created_at', 'updated_by',)
    list_filter = ('empleado__sucursal', 'tipo_incidencia', 'estado_incidencia',)
    date_hierarchy = 'fecha'
    autocomplete_fields = ('empleado', 'tipo_incidencia', 'empleado_obj',)
    search_fields = ('empleado__postulante__usuario__first_name', 'empleado__postulante__usuario__last_name', 'tipo_incidencia__nombre')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'monto')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    # Métodos
    def aceptar_incidencia(self, request, queryset):
        """Aceptar incidencias seleccionadas."""
        for incidencia in queryset:
            incidencia.estado_incidencia = 'APROBADA'
            incidencia.save()
        self.message_user(request, "Incidencias aprobadas correctamente.")
    aceptar_incidencia.short_description = "Aceptar incidencias seleccionadas"

    def rechazar_incidencia(self, request, queryset):
        """Rechazar incidencias seleccionadas."""
        for incidencia in queryset:
            incidencia.estado_incidencia = 'RECHAZADA'
            incidencia.save()
        self.message_user(request, "Incidencias rechazadas correctamente.")
    rechazar_incidencia.short_description = "Rechazar incidencias seleccionadas"

    def cambiar_incidencia(self, request, queryset):
        """Cambiar el estado de las incidencias seleccionadas."""
        for incidencia in queryset:
            incidencia.estado_incidencia = 'PENDIENTE'
            incidencia.save()
        self.message_user(request, "Incidencias cambiadas a pendiente correctamente.")
    cambiar_incidencia.short_description = "Cambiar incidencias seleccionadas a pendiente"
    # Acciones personalizadas
    actions = ['aceptar_incidencia', 'rechazar_incidencia', 'cambiar_incidencia']

@admin.register(ConfiguracionIncidenciasModel)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('incidencia', 'tipo_asistencia',)