from django.db import models
from base.models import BaseModel
from incidencia.models import IncidenciasEmpleados
from empleado.models import EmpleadoModel
# Create your models here.

class Nomia(BaseModel):
    empleado = models.ForeignKey(
        EmpleadoModel, 
        on_delete=models.PROTECT, 
        related_name="nomina_empleado", 
        verbose_name="Empleado",
        null=False,
        blank=False
    )
    incidencias = models.ManyToManyField(
        IncidenciasEmpleados, 
        related_name="nomina_incidencias", 
        verbose_name="Incidencias"
    )
    fecha_generacion = models.DateField(verbose_name="Fecha de Generación", help_text="Fecha en la que se generó la nómina", null=False, blank=False)
    # Datos de pago
    total_percepciones = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Total de Percepciones", 
        help_text="Total de percepciones del empleado", 
        null=False, 
        blank=False
    )
    total_deducciones = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Total de Deducciones", 
        help_text="Total de deducciones del empleado", 
        null=False, 
        blank=False
    )
    total_neto = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Total Neto", 
        help_text="Total neto a pagar al empleado", 
        null=False, 
        blank=False
    )
    # Fechas de pago
    fecha_pago = models.DateField(verbose_name="Fecha de Pago", help_text="Fecha en la que se realizó el pago", null=True, blank=True)
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio", help_text="Fecha de inicio del periodo de pago", null=True, blank=True) # la fecha inicio debe ser un dia mayor a la fecha de generacion
    fecha_fin = models.DateField(verbose_name="Fecha de Fin", help_text="Fecha de fin del periodo de pago", null=True, blank=True) # la fecha fin debe ser igual a la fecha de generacion
    estado_nomina = models.CharField(max_length=20, verbose_name="Estado de la Nómina", choices=[('PENDIENTE', 'Pendiente'), ('GENERADA', 'Generada'), ('CANCELADA', 'Cancelada')], default='PENDIENTE')
    class Meta:
        verbose_name = "Nómina"
        verbose_name_plural = "Nóminas"
        db_table = "nomina"
    def __str__(self):
        return f"Nómina de {self.empleado} - {self.fecha_generacion}"