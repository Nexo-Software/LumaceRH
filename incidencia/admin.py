from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import CategoriaIncidenciasModel, TablaCalculosIncidenciasModel, TipoIncidenciaModel, IncidenciasEmpleadoModel

@admin.register(CategoriaIncidenciasModel)
class CategoriaIncidenciasModelAdmin(ModelAdmin):
    list_display = ('nombre', 'descripcion', 'codigo')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('efecto',)
    fieldsets = (
        ('General', {
            'fields': ('nombre', 'descripcion', 'codigo', 'efecto')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by')
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

@admin.register(TablaCalculosIncidenciasModel)
class TablaCalculosIncidenciasModelAdmin(ModelAdmin):
    list_display = ('nombre', 'tipo_metodo', 'descripcion')
    search_fields = ('nombre', 'descripcion', 'formula')
    list_filter = ('tipo_metodo',)
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'tipo_metodo')
        }),
        ('Configuración de Cálculo', {
            'fields': ('monto_fijo', 'porcentaje', 'multiplicador', 'work_hours_per_day')
        }),
        ('Fórmula Personalizada', {
            'classes': ('collapse',),
            'fields': ('formula',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by')
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


@admin.register(TipoIncidenciaModel)
class TipoIncidenciaModelAdmin(ModelAdmin):
    list_display = ('nombre', 'codigo', 'categoria', 'metodo_calculo', 'es_acumulable', 'afecta_asistencia')
    search_fields = ('nombre', 'descripcion', 'codigo')
    list_filter = ('categoria', 'es_acumulable', 'es_aprobada', 'requiere_documentacion', 'afecta_asistencia')
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'codigo', 'categoria', 'metodo_calculo')
        }),
        ('Configuración de Acumulación', {
            'classes': ('collapse',),
            'fields': ('es_acumulable', 'conteo_acumulativo', 'tipo_efecto_acumulativo', 'periodo_reinicio')
        }),
        ('Configuración Adicional', {
            'fields': ('max_dias', 'es_aprobada', 'requiere_documentacion', 'afecta_asistencia')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by')
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


@admin.register(IncidenciasEmpleadoModel)
class IncidenciasEmpleadoModelAdmin(ModelAdmin):
    list_display = ('empleado', 'tipo_incidencia', 'incident_date', 'start_date', 'end_date', 'status', 'amount', 'processed_in_payroll')
    search_fields = ('empleado__nombre', 'empleado__apellido', 'details', 'tipo_incidencia__nombre')
    list_filter = ('status', 'tipo_incidencia', 'processed_in_payroll', 'is_generated', 'incident_date')
    date_hierarchy = 'incident_date'
    
    fieldsets = (
        ('Empleado e Incidencia', {
            'fields': ('empleado', 'tipo_incidencia', 'puesto_objetivo')
        }),
        ('Fechas y Duración', {
            'fields': ('incident_date', 'start_date', 'end_date', 'hours')
        }),
        ('Detalles y Monto', {
            'fields': ('details', 'amount')
        }),
        ('Estado y Seguimiento', {
            'fields': ('status', 'parent_incident', 'is_generated')
        }),
        ('Aprobación', {
            'fields': ('approval_date', 'approved_by', 'document')
        }),
        ('Procesamiento de Nómina', {
            'fields': ('processed_in_payroll', 'payroll_period')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by')
        })
    )
    
    readonly_fields = ('approval_date', 'approved_by', 'created_at', 'updated_at', 'created_by', 'updated_by', 'is_generated')
    
    actions = ['approve_incidents', 'reject_incidents', 'mark_as_processed']
    
    def approve_incidents(self, request, queryset):
        for incident in queryset.filter(status='PE'):
            incident.approve(request.user)
        self.message_user(request, f"{queryset.filter(status='PE').count()} incidencias aprobadas correctamente.")
    approve_incidents.short_description = "Aprobar incidencias seleccionadas"
    
    def reject_incidents(self, request, queryset):
        for incident in queryset.filter(status='PE'):
            incident.reject(request.user, "Rechazado desde administrador")
        self.message_user(request, f"{queryset.filter(status='PE').count()} incidencias rechazadas correctamente.")
    reject_incidents.short_description = "Rechazar incidencias seleccionadas"
    
    def mark_as_processed(self, request, queryset):
        period = request.POST.get('payroll_period', '')
        for incident in queryset.filter(status='AP'):
            incident.mark_as_processed(period)
        self.message_user(request, f"{queryset.filter(status='AP').count()} incidencias marcadas como procesadas.")
    mark_as_processed.short_description = "Marcar como procesadas en nómina"
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)