from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.utils.html import format_html
# Register your models here.
from .models import TurnosModel, SemanaModel, ProgramacionDiariaModel, AsignacionEmpleadoModel

@admin.register(TurnosModel)
class TurnosAdmin(admin.ModelAdmin):
    """Admin para los turnos de trabajo"""
    list_display = ('nombre', 'hora_inicio', 'hora_fin', 'sucursal', 'status')
    list_editable = ('status',)
    list_filter = ('sucursal', 'status')
    search_fields = ('nombre', 'sucursal__nombre')
    autocomplete_fields = ('sucursal',)
    
    fieldsets = (
        ('Información del turno', {
            'fields': ('nombre', 'hora_inicio', 'hora_fin', 'sucursal')
        }),
        ('Auditoría', {
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


@admin.register(SemanaModel)
class SemanaAdmin(ModelAdmin):
    """Admin para las semanas de trabajo"""
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'sucursal', 'status')
    list_editable = ('status',)
    list_filter = ('sucursal', 'status')
    search_fields = ('nombre', 'sucursal__nombre')
    autocomplete_fields = ('sucursal',)
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Información de la semana', {
            'fields': ('nombre', 'fecha_inicio', 'fecha_fin', 'sucursal')
        }),
        ('Auditoría', {
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


class AsignacionEmpleadoInline(TabularInline):
    """
    Inline para asignar empleados a una programación diaria
    """
    model = AsignacionEmpleadoModel
    extra = 1
    autocomplete_fields = ('empleado',)
    fields = ('empleado', 'observaciones')


@admin.register(ProgramacionDiariaModel)
class ProgramacionDiariaAdmin(ModelAdmin):
    """
    Admin para la programación diaria de horarios
    Permite asignar múltiples empleados a un día específico
    """
    list_display = ('dia', 'get_turno_display', 'semana', 'get_empleados_count', 'status')
    list_filter = ('semana', 'turno', 'status')
    search_fields = ('dia', 'turno__nombre', 'semana__nombre')
    autocomplete_fields = ('semana', 'turno')
    date_hierarchy = 'dia'
    
    inlines = [AsignacionEmpleadoInline]
    
    fieldsets = (
        ('Información de la programación', {
            'fields': ('semana', 'dia', 'turno', 'descripcion')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by', 'status'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    def get_turno_display(self, obj):
        """Muestra el turno con formato y horario"""
        return format_html(
            '<span style="padding: 5px 10px; border-radius: 5px; background-color: #4CAF50; color: white;">'
            '{} ({}:00 - {}:00)</span>',
            obj.turno.nombre, 
            obj.turno.hora_inicio.strftime('%H:%M'), 
            obj.turno.hora_fin.strftime('%H:%M')
        )
    get_turno_display.short_description = 'Turno'
    
    def get_empleados_count(self, obj):
        """Muestra el número de empleados asignados a esta programación"""
        count = obj.asignaciones.count()
        return format_html(
            '<span style="font-weight: bold;">{}</span> empleados',
            count
        )
    get_empleados_count.short_description = 'Empleados asignados'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AsignacionEmpleadoModel)
class AsignacionEmpleadoAdmin(ModelAdmin):
    """
    Admin para la asignación de empleados
    (Generalmente se usará a través del inline, pero es útil tenerlo por separado)
    """
    list_display = ('empleado', 'programacion', 'status')
    list_filter = ('programacion__dia', 'programacion__turno', 'status')
    search_fields = ('empleado__postulante__usuario__first_name', 'empleado__postulante__usuario__last_name')
    autocomplete_fields = ('programacion', 'empleado')
    
    fieldsets = (
        ('Información de la asignación', {
            'fields': ('programacion', 'empleado', 'observaciones')
        }),
        ('Auditoría', {
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