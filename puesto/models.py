from django.db import models
from base.models import BaseModel
from departamento.models import DepartamentoModel
from django.contrib.auth.models import User
# Create your models here.

class PuestoModel(BaseModel):
    # Información del puesto
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre del puesto', help_text='Nombre del puesto')
    departamento = models.ForeignKey(DepartamentoModel, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Departamento', help_text='Departamento al que pertenece el puesto', related_name='%(app_label)s_%(class)s_departamento')
    # Información del usuario
    # Métodos
    def __str__(self):
        return f'{self.nombre} - {self.departamento.nombre}'
    
    class Meta:
        verbose_name = 'Puesto'
        verbose_name_plural = 'Puestos'
        db_table = 'puestos'