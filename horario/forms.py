# Formularios
from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
# Modelos
from .models import TurnosModel, SemanaModel, ProgramacionDiariaModel, AsignacionEmpleadoModel

# Formulario para crear turnos
class TurnosModelForm(forms.ModelForm):
    class Meta:
        model = TurnosModel
        fields = [
            'nombre', 'hora_inicio', 'hora_fin',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

# Formularios de semana
class SemanaModelFormNombre(forms.ModelForm):
    class Meta:
        model = SemanaModel
        fields = [
            'nombre'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class SemanaModelFormFechas(forms.ModelForm):
    class Meta:
        model = SemanaModel
        fields = [
            'fecha_inicio', 'fecha_fin',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class SemanaModelFormSucursal(forms.ModelForm):
    class Meta:
        model = SemanaModel
        fields = [
            'sucursal',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

# Formulario de Horarios (Programacion Diaria)
class ProgramacionFormFecha(forms.ModelForm):
    class Meta:
        model = ProgramacionDiariaModel
        fields = [
            'semana', 'dia', 'turno'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # Poner el campo "dia" como un campo de fecha
        date_attrs = {'type': 'date'}
        self.fields['dia'].widget = forms.DateInput(attrs=date_attrs)


# Formulario asignacion de empleados
class AsignacionEmpleadoForm(forms.ModelForm):
    class Meta:
        model = AsignacionEmpleadoModel
        fields = [
            'programacion', 'empleado'
        ]

# Inlines forms
AsignacionEmpleadoFormSet = inlineformset_factory(
    ProgramacionDiariaModel,
    AsignacionEmpleadoModel,
    fields=('empleado',),
    extra=1,
    can_delete=False  # Si quieres permitir eliminar, ponlo a True
)