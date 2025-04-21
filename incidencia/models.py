from django.db import models
from base.models import BaseModel
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
        db_table = "incidencias_categoria"
    
    def __str__(self):
        return self.nombre

class FormulaIncidenciasModel(BaseModel):
    """
    Modelo que define las fórmulas personalizadas para incidencias
    Esto permite a cada empresa definir sus propias fórmulas
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    # Campos de formular
    
    class Meta:
        verbose_name = "Fórmula de Incidencias"
        verbose_name_plural = "Fórmulas de Incidencias"
        db_table = "incidencias_formula"
    
    def __str__(self):
        return self.nombre