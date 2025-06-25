from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from puesto.models import PuestoModel
from contrato.models import ContratoModel
from tinymce.models import HTMLField
# Create your models here.


# Modelo para el postulante
class PostulanteModel(BaseModel):
    # {nombre, apellido, correo, usuario}
    usuario = models.OneToOneField(User, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_usuario', null=False, blank=False)
    # Direccion
    calle = models.CharField(max_length=255, verbose_name='Calle', null=True, blank=True)
    numero = models.CharField(max_length=10, verbose_name='Número', null=True, blank=True)
    ciudad = models.CharField(max_length=255, verbose_name='Ciudad', null=True, blank=True)
    codigo_postal = models.CharField(max_length=10, verbose_name='Código Postal', null=True, blank=True)
    provincia = models.CharField(max_length=255, verbose_name='Provincia', null=True, blank=True)
    pais = models.CharField(max_length=255, verbose_name='País', null=True, blank=True)
    @property
    def direccion(self):
        # Devuelve la dirección completa del postulante en un formato legible (ej. Calle #Número, Ciudad, C.P. Código Postal. Provincia, País)
        return f'{self.calle} #{self.numero}, {self.ciudad}, C.P. {self.codigo_postal}. {self.provincia}, {self.pais}'
    direccion.fget.short_description = 'Dirección'
    # Datos de puesto
    puesto = models.ForeignKey(PuestoModel, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_puesto', null=False, blank=False)
    # Datos de contrato
    contrato = models.ForeignKey(ContratoModel, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_contrato', null=False, blank=False)
    # Notas
    notas = HTMLField(null=True, blank=True)
    # Estado del postulante
    ESTADO_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.puesto.nombre} - {self.contrato.tipo_contrato}"
    class Meta:
        verbose_name = "Postulante"
        verbose_name_plural = "Postulantes"
        db_table = "postulantes"

class EmpleadoModel(BaseModel):
    # {nombre, apellido, correo, usuario}
    postulante = models.OneToOneField(PostulanteModel, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_postulante', null=False, blank=False)
    # Datos de puesto
    puesto = models.ForeignKey(PuestoModel, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_puesto', null=True, blank=True)
    # Datos de contrato
    contrato = models.ForeignKey(ContratoModel, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_contrato', null=True, blank=True)
    @property
    def sueldo(self):
        """
        Devuelve el sueldo quincenal del postulante.
        """
        return self.contrato.salario_base * 15 if self.contrato else 0.0
    sueldo.fget.short_description = 'Sueldo'
    # Sucursal
    sucursal = models.ForeignKey('sucursal.SucursalModel', on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_sucursal', null=True, blank=True)
    # Notas
    notas = HTMLField(null=True, blank=True)
    fecha_contratacion = models.DateField(null=True, blank=True, verbose_name='Fecha de Contratación', help_text='Fecha de contratación del empleado')
    def __str__(self):
        return f"{self.postulante.usuario.first_name} {self.postulante.usuario.last_name} - {self.puesto.nombre}"
    class Meta:
        db_table = 'empleados'
        managed = True
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'