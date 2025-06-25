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
        return f"{self.nombre} ({self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')})"

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
        return f"{self.nombre} ({self.fecha_inicio} al {self.fecha_fin})"

class ProgramacionDiariaModel(BaseModel):
    """
    Modelo que define un día específico de la programación de horarios.
    Aquí se asignan múltiples empleados a un día y turno específicos.
    """
    semana = models.ForeignKey(
        SemanaModel,
        on_delete=models.CASCADE,
        related_name="programaciones",
        verbose_name="Semana"
    )
    dia = models.DateField(
        verbose_name="Día",
        help_text="Día de la programación"
    )
    turno = models.ForeignKey(
        TurnosModel,
        on_delete=models.PROTECT,
        related_name="programaciones",
        verbose_name="Turno"
    )
    descripcion = models.CharField(
        max_length=255,
        verbose_name="Descripción",
        blank=True, 
        null=True
    )
    
    class Meta:
        verbose_name = "Programación Diaria"
        verbose_name_plural = "Programaciones Diarias"
        db_table = "programacion_diaria"
        unique_together = ['semana', 'dia', 'turno']  # No puede haber duplicados
    
    def __str__(self):
        return f"Programación {self.dia} - {self.turno.nombre}"

class AsignacionEmpleadoModel(BaseModel):
    """
    Modelo que asigna un empleado a una programación diaria específica.
    """
    programacion = models.ForeignKey(
        ProgramacionDiariaModel,
        on_delete=models.CASCADE,
        related_name="asignaciones",
        verbose_name="Programación"
    )
    empleado = models.ForeignKey(
        EmpleadoModel,
        on_delete=models.PROTECT,
        related_name="asignaciones_horario",
        verbose_name="Empleado"
    )
    
    class Meta:
        verbose_name = "Asignación de Empleado"
        verbose_name_plural = "Asignaciones de Empleados"
        db_table = "asignacion_empleado"
        unique_together = ['programacion', 'empleado']  # Un empleado no puede estar dos veces en la misma programación
    
    def __str__(self):
        return f"{self.empleado} - {self.programacion}"