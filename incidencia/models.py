from django.db import models
from base.models import BaseModel
from empresa.models import EmpresaModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from empleado.models import EmpleadoModel
from puesto.models import PuestoModel
from ckeditor.fields import RichTextField
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

class IncidenciasEmpleadoModel(BaseModel):
    """
    Modelo que registra las incidencias aplicadas a los empleados
    """
    # Estados de la incidencia
    STATUS_CHOICES = [
        ('PE', 'Pendiente'),
        ('AP', 'Aprobada'),
        ('RE', 'Rechazada'),
        ('CA', 'Cancelada'),
        ('PR', 'Procesada'),
    ]
    
    # Relaciones principales
    empleado = models.ForeignKey(
        EmpleadoModel,
        on_delete=models.PROTECT,
        related_name="incidentes",
        verbose_name="Empleado"
    )
    tipo_incidencia = models.ForeignKey(
        TipoIncidenciaModel,
        on_delete=models.PROTECT,
        related_name="incidentes_empleado",
        verbose_name="Tipo de incidencia"
    )
    
    # Para incidencias que implican otro puesto (ej: encargados temporales)
    puesto_objetivo = models.ForeignKey(
        PuestoModel,
        on_delete=models.PROTECT,
        related_name="asignaciones_temporales",
        verbose_name="Puesto objetivo",
        null=True,
        blank=True,
        help_text="Para incidencias que implican cambio temporal de puesto"
    )
    
    # Fechas y duración
    incident_date = models.DateField(verbose_name="Fecha de incidencia")
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de fin", null=True, blank=True)
    
    # Para incidencias por hora
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Horas",
        help_text="Número de horas para incidencias por tiempo"
    )
    
    # Detalles
    details = RichTextField(verbose_name="Detalles", null=True, blank=True)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Monto",
        null=True,
        blank=True,
        help_text="Monto calculado o manual de la incidencia"
    )
    
    # Estado y seguimiento
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='PE',
        verbose_name="Estado"
    )
    parent_incident = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name="generated_incidents",
        verbose_name="Incidencia origen",
        null=True,
        blank=True,
        help_text="Para incidencias generadas automáticamente por acumulación"
    )
    is_generated = models.BooleanField(
        default=False,
        verbose_name="Generada automáticamente",
        help_text="Indica si esta incidencia fue generada automáticamente por acumulación"
    )
    
    # Aprobación
    approval_date = models.DateTimeField(verbose_name="Fecha de aprobación", null=True, blank=True)
    approved_by = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name="approved_incidents",
        verbose_name="Aprobado por",
        null=True,
        blank=True
    )
    
    # Documentación
    document = models.FileField(
        upload_to='incident_documents/',
        verbose_name="Documento de soporte",
        null=True,
        blank=True
    )
    
    # Procesamiento de nómina
    processed_in_payroll = models.BooleanField(
        default=False,
        verbose_name="Procesado en nómina"
    )
    payroll_period = models.CharField(
        max_length=20,
        verbose_name="Periodo de nómina",
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "Incidencia de empleado"
        verbose_name_plural = "Incidencias de empleados"
        db_table = "employee_incidents"
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.incident_type.name} - {self.incident_date}"
    
    @property
    def duration_days(self):
        """Calcula la duración en días de la incidencia"""
        if not self.end_date or self.end_date == self.start_date:
            return 1
        return (self.end_date - self.start_date).days + 1
    
    @property
    def is_active(self):
        """Determina si la incidencia está activa en la fecha actual"""
        today = timezone.now().date()
        if self.status not in ['AP', 'PR']:
            return False
        if today < self.start_date:
            return False
        if self.end_date and today > self.end_date:
            return False
        return True
    
    def calculate_amount(self):
        """Calcula el monto de la incidencia según su tipo y método de cálculo"""
        if not hasattr(self, 'incident_type') or not self.incident_type:
            return None
            
        # Si no tiene efecto económico, no hay monto
        if self.incident_type.category.effect == 'NONE':
            return None
            
        # Si no tiene método de cálculo, no podemos calcular
        if not self.incident_type.calculation_method:
            return None
            
        # Obtenemos el salario base del empleado (asumiendo que existe un campo daily_salary)
        base_salary = getattr(self.employee, 'daily_salary', 0)
        if not base_salary and hasattr(self.employee, 'current_contract'):
            # Intentamos obtenerlo del contrato
            if self.employee.current_contract and hasattr(self.employee.current_contract, 'salary'):
                if self.employee.current_contract.salary_frequency == 'D':  # Diario
                    base_salary = self.employee.current_contract.salary
                elif self.employee.current_contract.salary_frequency == 'M':  # Mensual
                    base_salary = self.employee.current_contract.salary / 30  # Aproximación
                # Agregar otros casos según sea necesario
        
        # Calculamos el monto
        return self.incident_type.calculation_method.calculate(
            base_salary=base_salary,
            days=self.duration_days,
            hours=self.hours or 0,
            target_position=self.target_position
        )
    
    def save(self, *args, **kwargs):
        # Establecer fecha de fin igual a inicio si no se especifica
        if not self.end_date:
            self.end_date = self.start_date
            
        # Calcular monto automáticamente si no se especifica y es calculable
        if self.amount is None and self.incident_type and self.incident_type.category.effect in ['ADD', 'SUB']:
            self.amount = self.calculate_amount()
            
        # Guardar el objeto
        super().save(*args, **kwargs)
        
        # Si es acumulativa, verificar si debe generar otra incidencia
        if (self.status == 'AP' and self.incident_type and self.incident_type.is_cumulative 
                and self.incident_type.cumulative_effect_type):
            self._check_cumulative_effect()
    
    def _check_cumulative_effect(self):
        """Verifica si debe generarse una incidencia por acumulación"""
        # Obtener el tipo de incidencia y contador acumulativo
        incident_type = self.incident_type
        cumulative_count = incident_type.cumulative_count
        
        # Determinar el período de búsqueda según el período de reinicio
        start_date = None
        today = timezone.now().date()
        
        if incident_type.reset_period == 'DAILY':
            start_date = today
        elif incident_type.reset_period == 'WEEKLY':
            start_date = today - timezone.timedelta(days=today.weekday())
        elif incident_type.reset_period == 'BIWEEKLY':
            # Simplificación: primer o segunda quincena del mes
            if today.day <= 15:
                start_date = today.replace(day=1)
            else:
                start_date = today.replace(day=16)
        elif incident_type.reset_period == 'MONTHLY':
            start_date = today.replace(day=1)
        
        # Contar incidencias acumuladas
        count_filter = {
            'employee': self.employee,
            'incident_type': incident_type,
            'status': 'AP'  # Solo aprobadas
        }
        
        if start_date:
            count_filter['incident_date__gte'] = start_date
            
        # Evitar contar incidencias generadas automáticamente
        count_filter['is_generated'] = False
        
        accumulated_count = IncidenciasEmpleadoModel.objects.filter(**count_filter).count()
        
        # Si alcanzó el límite, generar la incidencia acumulativa
        if accumulated_count >= cumulative_count:
            # Crear la incidencia resultante
            IncidenciasEmpleadoModel.objects.create(
                employee=self.employee,
                incident_type=incident_type.cumulative_effect_type,
                incident_date=today,
                start_date=today,
                end_date=today,
                details=f"Generada automáticamente por acumulación de {accumulated_count} incidencias de tipo {incident_type.name}",
                status='AP',  # Automáticamente aprobada
                parent_incident=self,
                is_generated=True,
                approved_by=self.approved_by,
                created_by=self.created_by or self.approved_by,  # AÑADIR ESTA LÍNEA
                updated_by=self.created_by or self.approved_by   # AÑADIR ESTA LÍNEA
            )
            
            # Opcional: marcar las incidencias acumuladas como "consumidas"
            #if incident_type.reset_period != 'NEVER':
            #    EmployeeIncident.objects.filter(**count_filter).update(
            #        details=models.F('details') + "\nContabilizada en incidencia acumulativa."
            #    )
            
    
    def approve(self, user):
        """Aprueba la incidencia"""
        if self.status == 'PE':
            self.status = 'AP'
            self.approval_date = timezone.now()
            self.approved_by = user
            self.save()
    
    def reject(self, user, reason=None):
        """Rechaza la incidencia"""
        if self.status == 'PE':
            self.status = 'RE'
            self.approval_date = timezone.now()
            self.approved_by = user
            if reason:
                self.details = f"{self.details or ''}\n\nRechazado: {reason}".strip()
            self.save()
            
    def mark_as_processed(self, payroll_period=None):
        """Marca la incidencia como procesada en nómina"""
        if self.status == 'AP':
            self.status = 'PR'
            self.processed_in_payroll = True
            if payroll_period:
                self.payroll_period = payroll_period
            self.save()