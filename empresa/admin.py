from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import EmpresaModel
from django.core.mail import send_mail

@admin.register(EmpresaModel)
class EmpresaAdmin(ModelAdmin):
    """Admin para la empresa"""
    list_display = ('razon_social', 'nombre_comercial', 'direccion', 'status')
    list_editable = ('status',)
    search_fields = ('razon_social', 'nombre_comercial',)
    list_per_page = 10
    fieldsets = (
        ('Información de la empresa', {
            'fields': ('razon_social', 'nombre_comercial')
        }),
        ('Dirección', {
            'fields': ('calle', 'numero', 'ciudad', 'codigo_postal', 'provincia', 'pais')
        }),
        ('Datos de contacto', {
            'fields': ('telefono', 'fax', 'email', 'web')
        }),
        ('Datos de identificación fiscal', {
            'fields': ('rfc',)
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
            # Enviar correo de confirmación al administrador
            send_mail(
                'La empresa se a creado',
                'Este es el primer paso, el sistema funciona correctamente.',
                'lmcervantessuarez@gmail.com',  # From
                ['luismariosuarez@lumace.cloud'],  # To
                fail_silently=False,
            )
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)