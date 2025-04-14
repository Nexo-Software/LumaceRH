from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from puesto.models import PuestoModel
from contrato.models import ContratoModel
from ckeditor.fields import RichTextField
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
        return f'{self.calle} # {self.numero}, {self.ciudad}, C.P. {self.codigo_postal}. {self.provincia}, {self.pais}'
    direccion.fget.short_description = 'Dirección'
    # Datos de puesto
    puesto = models.ForeignKey(PuestoModel, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_puesto', null=True, blank=True)
    # Datos de contrato
    contrato = models.ForeignKey(ContratoModel, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_contrato', null=True, blank=True)
    # Notas
    notas = RichTextField(null=True, blank=True)
    # Estado del postulante
    ESTADO_CHOICES = (
        ('P', 'Pendiente'),
        ('A', 'Aceptado'),
        ('R', 'Rechazado'),
    )
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.puesto.nombre} - {self.contrato.tipo_contrato}"
    class Meta:
        verbose_name = "Postulante"
        verbose_name_plural = "Postulantes"
        db_table = "empleado_postulante"

class EmpleadoModel(BaseModel):
    # {nombre, apellido, correo, usuario}
    postulante = models.OneToOneField(PostulanteModel, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_postulante', null=False, blank=False)
    # Datos de puesto
    puesto = models.ForeignKey(PuestoModel, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_puesto', null=True, blank=True)
    # Datos de contrato
    contrato = models.ForeignKey(ContratoModel, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_contrato', null=True, blank=True)
    # Sucursal
    sucursal = models.ForeignKey('sucursal.SucursalModel', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_sucursal', null=True, blank=True)
    # Notas
    notas = RichTextField(null=True, blank=True)