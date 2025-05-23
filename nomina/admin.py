from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
# Register your models here.
from .models import NomiaModel

@admin.register(NomiaModel)
class NominaAdmin(ModelAdmin):
    """Admin para la nómina de empleados"""
    
    def get_estado_display(self, obj):
        """Muestra el estado de la nómina con formato visual."""
        estados = {
            'PENDIENTE': ('Pendiente', '#FFA500', '#fff'),  # Naranja para pendiente
            'GENERADA': ('Generada', '#4CAF50', '#fff'),   # Verde para generada
            'CANCELADA': ('Cancelada', '#F44336', '#fff'),  # Rojo para cancelada
        }
        
        label, bg_color, text_color = estados.get(obj.estado_nomina, ('Desconocido', '#999', '#fff'))
        
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 5px 10px; '
            'border-radius: 10px; font-weight: bold; font-size: 0.9em;">{}</span>',
            bg_color, text_color, label
        )

    get_estado_display.short_description = 'Estado'

    def get_total_percepciones(self, obj):
        valor = obj.total_percepciones if obj.total_percepciones is not None else 0
        return format_html(
            f'<span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">$ {valor}</span>')
    get_total_percepciones.short_description = 'Percepciones'

    def get_total_deducciones(self, obj):
        valor = obj.total_deducciones if obj.total_deducciones is not None else 0
        return format_html(f'<span style="background-color: #F44336; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">$ {valor}</span>')
    get_total_deducciones.short_description = 'Deducciones'

    def get_total_neto(self, obj):
        valor = obj.total_neto if obj.total_neto is not None else 0
        return format_html(f'<span style="background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">$ {valor}</span>')
    get_total_neto.short_description = 'Sueldo Final'
    # Campos a mostrar en la lista de nóminas
    list_display = ('empleado', 'fecha_generacion', 'get_total_percepciones',
                    'get_total_deducciones', 'get_total_neto', 'get_estado_display', 'estado_nomina')
    list_editable = ('estado_nomina',)
    # Filtros para la lista de nóminas
    list_filter = ('estado_nomina', 'fecha_generacion', 'empleado__sucursal')
    
    # Búsqueda por campos relevantes
    search_fields = ('empleado__postulante__usuario__first_name', 
                     'empleado__postulante__usuario__last_name')
    
    # Campos de autocompletado para las relaciones
    autocomplete_fields = ('empleado',)
    
    # Filtro por fechas
    date_hierarchy = 'fecha_generacion'
    
    # Agrupación de campos en el formulario
    fieldsets = (
        ('Información básica', {
            'fields': ('empleado', 'fecha_generacion', 'estado_nomina')
        }),
        ('Periodo de pago', {
            'fields': ('fecha_inicio', 'fecha_fin', 'fecha_pago')
        }),
        ('Montos', {
            'fields': ('total_percepciones', 'total_deducciones', 'total_neto')
        }),
        ('Incidencias', {
            'fields': ('incidencias',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by', 'status'),
            'classes': ('collapse',)
        })
    )
    
    # Campos de solo lectura
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'total_percepciones', 'total_deducciones', 'total_neto')
    
    def save_model(self, request, obj, form, change):
        """Asigna el usuario que crea o actualiza el registro."""
        if not change:  # Si es nuevo registro
            obj.created_by = request.user
            obj.updated_by = request.user
        else:  # Si es actualización
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    # Método para calcular totales automáticamente (opcional)
    def calculate_totals(self, request, queryset):
        """Acción para calcular los totales de las nóminas seleccionadas."""
        for nomina in queryset:
            # Cambiar el estado a GENERADA
            nomina.estado_nomina = 'GENERADA'
            nomina.save()
        self.message_user(request, f"{queryset.count()} nóminas actualizadas correctamente.")
    calculate_totals.short_description = "Calcular totales de nóminas seleccionadas"
    
    # Acciones personalizadas
    actions = ['calculate_totals']