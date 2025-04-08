from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from puesto.models import PuestoModel
from contrato.models import ContratoModel
from ckeditor.fields import RichTextField
# Create your models here.

class PostulanteModel(BaseModel):
    # {nombre, apellido, correo, usuario}
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_usuario', null=False, blank=False)
    # Datos de puesto
    puesto = models.ForeignKey(PuestoModel, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_puesto', null=True, blank=True)
    # Datos de contrato
    contrato = models.ForeignKey(ContratoModel, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_contrato', null=True, blank=True)
    # Notas
    notas = RichTextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.puesto.nombre} - {self.contrato.tipo_contrato}"
    class Meta:
        verbose_name = "Postulante"
        verbose_name_plural = "Postulantes"
        db_table = "empleado_postulante"