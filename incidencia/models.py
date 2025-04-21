from django.db import models
from base.models import BaseModel
from empleado.models import EmpleadoModel
from contrato.models import ContratoModel
from ckeditor.fields import RichTextField
# Create your models here.

# Nuevos modelos para manejar las incidencias de forma más eficiente (Categoria, Formulas, Tipos, Incidencias)
class CategoriaIncidenciasModel(BaseModel):
    """
    Modelo que define las categorías principales de incidencias (Percepción, Deducción, etc.)
    Esto permite a cada empresa definir sus propias categorías
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    codigo = models.CharField(max_length=20, verbose_name="Código", null=True, blank=True)
    
    # Efecto en nómina (opciones básicas)
    EFFECT_CHOICES = [
        ('ADD', 'Percepción (suma)'),
        ('SUB', 'Deducción (resta)'),
        ('NONE', 'Sin efecto económico'),
        ('ACCUM', 'Acumulativa'),
    ]
    
    efecto = models.CharField( # Escoger entre las opciones
        max_length=5, 
        choices=EFFECT_CHOICES, 
        default='NONE',
        verbose_name="Efecto en nómina"
    )
    class Meta:
        verbose_name = "Categoría de Incidencias"
        verbose_name_plural = "Categorías de Incidencias"
        db_table = "categoria_incidencias"
    
    def __str__(self):
        return self.nombre

class TiposFormulasModel(BaseModel):
    """
    Modelo que define los tipos de fórmulas (Fijo, Porcentaje, etc.)
    Esto permite a cada empresa definir sus propios tipos de fórmulas
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    codigo = models.CharField(max_length=3, verbose_name="Código", null=True, blank=True, unique=True, help_text="Código único para identificar el tipo de fórmula")
    class Meta:
        verbose_name = "Tipo de Fórmula"
        verbose_name_plural = "Tipos de Fórmulas"
        db_table = "tipo_formula_incidencias"
    
    def __str__(self):
        return self.nombre

class FormulaIncidenciasModel(BaseModel):
    """
    Modelo que define las fórmulas personalizadas para incidencias
    Esto permite a cada empresa definir sus propias fórmulas
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    codigo = models.ForeignKey(
        TiposFormulasModel, 
        on_delete=models.PROTECT, 
        related_name="formula", 
        verbose_name="Tipo de Fórmula"
    )
    formula_detalle = models.TextField(verbose_name="Detalle de la Fórmula", null=True, blank=True)
    class Meta:
        verbose_name = "Fórmula de Incidencias"
        verbose_name_plural = "Fórmulas de Incidencias"
        db_table = "formulas_incidencias"
    
    def __str__(self):
        return self.nombre

class TipoIncidenciasModel(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    categoria = models.ForeignKey(
        CategoriaIncidenciasModel, 
        on_delete=models.PROTECT, 
        related_name="tipo_incidencia", 
        verbose_name="Categoría de Incidencia"
    )
    formula = models.ForeignKey(
        FormulaIncidenciasModel, 
        on_delete=models.PROTECT, 
        related_name="tipo_incidencia", 
        verbose_name="Fórmula de Incidencia"
    )
    referencia_monto = models.ForeignKey(
        ContratoModel, 
        on_delete=models.PROTECT, 
        related_name="tipo_incidencia", 
        verbose_name="Referencia de Monto"
    )
    class Meta:
        verbose_name = "Tipo de Incidencia"
        verbose_name_plural = "Tipos de Incidencias"
        db_table = "tipo_incidencias"
    def __str__(self):
        return self.nombre

ESTADOS_INCIDENCIA = [
    ('PENDIENTE', 'Pendiente'),
    ('APROBADA', 'Aprobada'),
    ('RECHAZADA', 'Rechazada'),
]
class IncidenciasEmpleados(BaseModel):
    empleado = models.ForeignKey(
        EmpleadoModel, 
        on_delete=models.PROTECT, 
        related_name="incidencias_empleado", 
        verbose_name="Empleado"
    )
    tipo_incidencia = models.ForeignKey(
        TipoIncidenciasModel, 
        on_delete=models.PROTECT, 
        related_name="incidencias_tipo", 
        verbose_name="Tipo de Incidencia"
    )
    fecha = models.DateField(verbose_name="Fecha de la Incidencia")
    estado_incidencia = models.CharField(
        max_length=10, 
        choices=ESTADOS_INCIDENCIA, 
        default='PENDIENTE', 
        verbose_name="Estado de la Incidencia"
    )
    class Meta:
        verbose_name = "Incidencia de Empleado"
        verbose_name_plural = "Incidencias de Empleados"
        db_table = "incidencias_empleados"
    def __str__(self):
        return f"{self.empleado} - {self.tipo_incidencia} - {self.fecha}"