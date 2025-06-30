from django.db import models
from base.models import BaseModel
# Create your models here.

TIPO_CONTRATO = {
    ('Indefinido', 'Indefinido'),
    ('Definido', 'Definido'),
    ('Servicio', 'Servicio'),
    ('Temporal', 'Temporal'),
}

class ContratoModel(BaseModel):
    # Información básica
    nombre = models.CharField(max_length=100, null=True, blank=True)
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO, null=False, blank=False)
    # No es por hora de trabajo, es por dia de la semana
    horas_trabajo = models.IntegerField(null=False, blank=False, default=0, help_text='Horas de trabajo diarias')
    # Información de salario
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00, help_text='Salario diario')
    # Datos de fecha
    fecha_inicio = models.DateField(null=False, blank=False)
    fecha_fin = models.DateField(null=True, blank=True)
    personalizado = models.BooleanField(default=False, help_text='Indica si el contrato es personalizado', verbose_name='Contrato Personalizado', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        db_table = 'contratos'
    def __str__(self):
        return f"{self.nombre} - {self.tipo_contrato} - {self.horas_trabajo} horas - ${self.salario_base}"