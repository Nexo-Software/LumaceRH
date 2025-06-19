from django import forms

import empleado
from .models import NominaModel
from crispy_forms.helper import FormHelper
from empleado.models import EmpleadoModel
from incidencia.models import IncidenciasEmpleados


class EmpleadoNominaForm(forms.ModelForm):
    """
    Formulario para seleccionar un empleado para la nómina.
    """

    class Meta:
        model = NominaModel
        fields = ['empleado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class FechasPagoNominaForm(forms.ModelForm):
    """
    Formulario para seleccionar las fechas de pago de la nómina.
    """

    class Meta:
        model = NominaModel
        fields = ['fecha_inicio', 'fecha_fin', 'fecha_pago']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # Campos
        self.fields['fecha_inicio'].label = 'Fecha de Inicio'
        self.fields['fecha_fin'].label = 'Fecha de Fin'
        self.fields['fecha_pago'].label = 'Fecha de Pago'
        # Configurar como campos de fecha HTML5
        date_attrs = {'type': 'date'}
        self.fields['fecha_inicio'].widget = forms.DateInput(attrs=date_attrs)
        self.fields['fecha_fin'].widget = forms.DateInput(attrs=date_attrs)
        self.fields['fecha_pago'].widget = forms.DateInput(attrs=date_attrs)
        # Hacer que los campos de fecha sean obligatorios
        self.fields['fecha_inicio'].required = True
        self.fields['fecha_fin'].required = True
        self.fields['fecha_pago'].required = True

class IncidenciasNominaForm(forms.ModelForm):
    """
    Formulario para seleccionar incidencias de un empleado para la nómina.
    """

    class Meta:
        model = NominaModel
        fields = ['incidencias']

    def __init__(self, *args, **kwargs):
        self.empleado = kwargs.pop('empleado', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # Campos
        self.fields['incidencias'].label = 'Seleccionar Incidencias aprobadas'
        self.fields['incidencias'].queryset = IncidenciasEmpleados.objects.filter(estado_incidencia='APROBADA', empleado=self.empleado).order_by('fecha')


