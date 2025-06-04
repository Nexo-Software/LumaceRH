from django.db import models
from empresa.models import EmpresaModel
from base.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.

class DepartamentoModel(BaseModel):
    nombre = models.CharField(max_length=50, verbose_name="Nombre del departamento", blank=False, null=False)
    #sucursal = models.ForeignKey(SucursalModel, on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_departamentos", verbose_name="Sucursal")
    empresa = models.ForeignKey(EmpresaModel, on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_departamentos", verbose_name="Empresa", blank=False, null=False)
    encargado = models.ForeignKey(User, on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_encargado", verbose_name="Encargado", blank=True, null=True)
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        db_table = "departamento"
    def __str__(self):
        return self.nombre