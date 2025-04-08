from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from puesto.models import PuestoModel
from contrato.models import ContratoModel
from ckeditor.fields import RichTextField
# Create your models here.

class Postulante(BaseModel):
    # {nombre, apellido, correo, usuario}
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_usuario', null=False, blank=False)
    # Datos de puesto
    puesto = models.ForeignKey(PuestoModel, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_puesto', null=True, blank=True)
    # Datos de contrato
    contrato = models.ForeignKey(ContratoModel, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_contrato', null=True, blank=True)
    # Notas
    notas = RichTextField(null=True, blank=True)