from django.db import models
from base.models import BaseModel
from empresa.models import EmpresaModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here.
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

class TablaCalculosIncidenciasModel(BaseModel):
    """
    Modelo que define los métodos de cálculo para incidencias
    Esto permite configurar diferentes fórmulas para calcular percepciones/deducciones
    """
    METHOD_TYPES = [
        ('FIXED', 'Monto fijo'),
        ('PERCENTAGE', 'Porcentaje del salario'),
        ('DAILY', 'Días de salario'),
        ('HOURLY', 'Horas (salario diario / horas jornada)'),
        ('POSITION_DIFF', 'Diferencia entre puestos'),
        ('CUSTOM', 'Fórmula personalizada'),
    ]
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    tipo_metodo = models.CharField( # Escoger entre las opciones definidas
        max_length=20, 
        choices=METHOD_TYPES, 
        verbose_name="Tipo de método"
    )
    
    # Para montos fijos
    monto_fijo = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Monto fijo"
    )
    
    # Para porcentajes
    porcentaje = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Porcentaje",
        validators=[MinValueValidator(0)]
    )
    
    # Para días o multiplicadores
    multiplicador = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Multiplicador",
        help_text="Factor multiplicador (ej: 1.5 para un día y medio)"
    )
    
    # Para cálculos basados en horas
    work_hours_per_day = models.PositiveSmallIntegerField(
        default=8,
        verbose_name="Horas por jornada",
        help_text="Horas de jornada laboral para cálculo de hora extra"
    )
    
    # Para fórmulas personalizadas
    formula = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Fórmula personalizada",
        help_text="Fórmula usando variables como {salary}, {days}, {hours}, etc."
    )
    
    class Meta:
        verbose_name = "Método de cálculo"
        verbose_name_plural = "Métodos de cálculo"
        db_table = "metodos_calculo_incidencias"
    
    def __str__(self):
        return self.nombre
    
    def calculate(self, base_salary, days=1, hours=0, target_position=None):
        """
        Calcula el monto según el método configurado
        
        :param base_salary: Salario diario del empleado
        :param days: Número de días aplicables
        :param hours: Número de horas aplicables (para cálculos por hora)
        :param target_position: Puesto objetivo (para cálculos de diferencia de puestos)
        :return: Monto calculado
        """
        if self.method_type == 'FIXED':
            return self.fixed_amount * days
        
        elif self.method_type == 'PERCENTAGE':
            return (base_salary * (self.percentage / 100)) * days
        
        elif self.method_type == 'DAILY':
            return base_salary * (self.multiplier or 1) * days
        
        elif self.method_type == 'HOURLY':
            hourly_rate = base_salary / (self.work_hours_per_day or 8)
            return hourly_rate * hours * (self.multiplier or 1)
        
        elif self.method_type == 'POSITION_DIFF' and target_position:
            # Asumiendo que tenemos acceso al salario base del puesto objetivo
            target_salary = getattr(target_position, 'base_salary', 0)
            return (target_salary - base_salary) * days
        
        elif self.method_type == 'CUSTOM' and self.formula:
            # Implementación básica - en producción usaría una solución más segura
            # como simpleeval para evaluar expresiones sin riesgos de seguridad
            try:
                context = {
                    'salary': base_salary,
                    'days': days,
                    'hours': hours,
                }
                # Esto es simplificado - en producción usaría un evaluador seguro
                # return eval(self.formula, {"__builtins__": {}}, context)
                return 0  # Por seguridad, retornamos 0 en este ejemplo
            except:
                return 0
        
        return 0

class TipoIncidenciaModel(BaseModel):
    """
    Modelo que define los tipos específicos de incidencias que pueden aplicarse
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    codigo = models.CharField(max_length=20, verbose_name="Código", null=True, blank=True)
    
    # Categorización y cálculo
    categoria = models.ForeignKey(
        CategoriaIncidenciasModel,
        on_delete=models.PROTECT,
        related_name="incident_types",
        verbose_name="Categoría"
    )
    metodo_calculo = models.ForeignKey(
        TablaCalculosIncidenciasModel,
        on_delete=models.PROTECT,
        related_name="incident_types",
        verbose_name="Método de cálculo",
        null=True,
        blank=True,
        help_text="Método de cálculo para percepción/deducción. No aplicable para incidencias sin efecto económico."
    )
    
    # Configuración para incidencias acumulativas
    es_acumulable = models.BooleanField(
        default=False,
        verbose_name="Es acumulativa",
        help_text="Indica si esta incidencia se acumula hasta llegar a cierto número para generar un efecto"
    )
    conteo_acumulativo = models.PositiveSmallIntegerField(
        default=3,
        verbose_name="Conteo acumulativo",
        help_text="Número de incidencias que deben acumularse para generar el efecto"
    )
    tipo_efecto_acumulativo = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name="cumulative_sources",
        verbose_name="Incidencia resultante",
        null=True,
        blank=True,
        help_text="Tipo de incidencia que se genera al acumular el conteo especificado"
    )
    periodo_reinicio = models.CharField(
        max_length=20,
        choices=[
            ('NEVER', 'Nunca'),
            ('DAILY', 'Diario'),
            ('WEEKLY', 'Semanal'),
            ('BIWEEKLY', 'Quincenal'),
            ('MONTHLY', 'Mensual'),
        ],
        default='NEVER',
        verbose_name="Período de reinicio",
        help_text="Cuándo se reinicia el contador acumulativo"
    )
    
    # Configuración adicional
    max_dias = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Días máximos",
        help_text="Máximo de días permitidos (0 = sin límite)"
    )
    es_aprobada = models.BooleanField(
        default=True,
        verbose_name="Requiere aprobación"
    )
    requiere_documentacion = models.BooleanField(
        default=False,
        verbose_name="Requiere documentación"
    )
    afecta_asistencia = models.BooleanField(
        default=False,
        verbose_name="Afecta asistencia",
        help_text="Indica si esta incidencia se considera una inasistencia"
    )
    
    
    class Meta:
        verbose_name = "Tipo de incidencia"
        verbose_name_plural = "Tipos de incidencias"
        db_table = "tipos_incidencias"
    
    def __str__(self):
        category_name = self.categoria.nombre if self.categoria else "Sin categoría"
        return f"{self.nombre} ({category_name})"
    
    def clean(self):
        # Validar que si es acumulativa, tenga definido el efecto
        if self.es_acumulable and not self.tipo_efecto_acumulativo:
            raise ValidationError(
                {'tipo_efecto_acumulativo': 'Para incidencias acumulativas debe especificar la incidencia resultante'}
            )
        
        # Validar que tenga método de cálculo si es percepción o deducción
        if (self.categoria and self.categoria.codigo in ['ADD', 'SUB']) and not self.metodo_calculo:
            raise ValidationError(
                {'metodo_calculo': 'Las incidencias de tipo percepción o deducción requieren un método de cálculo'}
            )