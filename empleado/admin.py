from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
# Register your models here.
from .models import EmpleadoModel, PostulanteModel

@admin.register(PostulanteModel)
class PostulanteAdmin(ModelAdmin):
    def get_estado_display(self, obj):
        """Muestra el estado del postulante con formato visual."""
        estados = {
            'P': ('Pendiente', '#FFA500', '#fff'),  # Naranja para pendiente
            'A': ('Aceptado', '#4CAF50', '#fff'),   # Verde para aceptado
            'R': ('Rechazado', '#F44336', '#fff'),  # Rojo para rechazado
        }
        
        label, bg_color, text_color = estados.get(obj.estado, ('Desconocido', '#999', '#fff'))
        
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 5px 10px; '
            'border-radius: 10px; font-weight: bold; font-size: 0.9em;">{}</span>',
            bg_color, text_color, label
        )
    
    get_estado_display.short_description = 'Estado'
    
    # Actualiza list_display para usar el nuevo método en lugar del campo estado directamente
    list_display = ('usuario__first_name', 'puesto', 'contrato', 'direccion', 'get_estado_display')
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
    list_display = ('postulante', 'puesto', 'contrato', 'get_sueldo', 'sucursal', 'status')
    list_filter = ('status', 'puesto', 'sucursal')
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
    def get_sueldo(self, obj):
        salario_base = obj.contrato.salario_base
        quincena = salario_base * 15
        # redondear (9,999.90) a (10,000.00)
        quincena = round(quincena, 2)
        return f"${quincena:,.2f}"
    get_sueldo.short_description = 'Sueldo'
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)