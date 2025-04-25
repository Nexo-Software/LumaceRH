from django.db import models
from base.models import BaseModel
from empleado.models import EmpleadoModel
from sucursal.models import SucursalModel

# Create your models here.

class TurnosModel(BaseModel):
    """
    Modelo que define los turnos de trabajo.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    sucursal = models.ForeignKey(
        SucursalModel, 
        on_delete=models.PROTECT, 
        related_name="turno_sucursal", 
        verbose_name="Sucursal"
    )
    
    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        db_table = "turno"
    
    def __str__(self):
        return self.nombre
class SemanaModel(BaseModel):
    """
    Modelo que define una semana de trabajo.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    sucursal = models.ForeignKey(
        SucursalModel, 
        on_delete=models.PROTECT, 
        related_name="semana_sucursal", 
        verbose_name="Sucursal"
    )
    class Meta:
        verbose_name = "Semana"
        verbose_name_plural = "Semanas"
        db_table = "semana"
    
    def __str__(self):
        return self.nombre

class HorarioModel(BaseModel):
    # Usar un inline (tabularinline) para poner a los empleados en el admin de horarios
    """
    Modelo que define el horario de trabajo de un empleado.
    """
    dia = models.DateField(verbose_name="Día", help_text="Día de la semana", null=False, blank=False)
    turno = models.ForeignKey(
        TurnosModel, 
        on_delete=models.PROTECT, 
        related_name="horario_turno", 
        verbose_name="Turno",
        null=False, 
        blank=False
    )
    empleado = models.ForeignKey(
        EmpleadoModel, 
        on_delete=models.PROTECT, 
        related_name="horario_empleado", 
        verbose_name="Empleado",
        null=False, 
        blank=False
    )
    semana = models.ForeignKey(
        SemanaModel, 
        on_delete=models.PROTECT, 
        related_name="horario_semana", 
        verbose_name="Semana",
        null=False, 
        blank=False
    )
    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        db_table = "horario"
    def __str__(self):
        return f"Horario de {self.empleado} - {self.dia} - {self.turno}"