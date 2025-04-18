from django.db import models
from base.models import BaseModel
# Create your models here.

TIPO_CONTRATO = {
    ('P', 'Indefinido'),
    ('D', 'Definido'),
    ('S', 'Servicio'),
    ('T', 'Temporal'),
}

FRECUENCIA_PAGO = {
    ('D', 'Diario'),
    ('S', 'Semanal'),
    ('Q', 'Quincenal'),
    ('M', 'Mensual'),
    ('A', 'Anual'),
}

class ContratoModel(BaseModel):
    # Información básica
    nombre = models.CharField(max_length=100, null=True, blank=True)
    tipo_contrato = models.CharField(max_length=1, choices=TIPO_CONTRATO, null=False, blank=False)
    # No es por hora de trabajo, es por dia de la semana
    #horas_trabajo = models.IntegerField(null=False, blank=False)
    # Información de salario
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    frecuencia_pago = models.CharField(max_length=1, choices=FRECUENCIA_PAGO, null=False, blank=False)
    # Datos de fecha
    fecha_inicio = models.DateField(null=False, blank=False)
    fecha_fin = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.get_tipo_contrato_display()} - {self.salario_base} {self.get_frecuencia_pago_display()}'
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        db_table = 'contratos'