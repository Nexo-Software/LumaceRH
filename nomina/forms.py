from django import forms
from .models import NomiaModel
from crispy_forms.helper import FormHelper
from empleado.models import EmpleadoModel


class EmpleadoNominaForm(forms.ModelForm):
    """
    Formulario para seleccionar un empleado para la nómina.
    """

    class Meta:
        model = EmpleadoModel
        fields = ['postulante']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # Campos
        self.fields['postulante'].label = 'Seleccionar Empleado'
        self.fields['postulante'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seleccione un empleado',
        })
        # Como cambio el contenido del campo 'postulante' para que muestre el nombre del usuario asociado al postulante
        self.fields['postulante'].label_from_instance = lambda \
                obj: f"{obj.usuario.first_name} {obj.usuario.last_name} - {obj.puesto.nombre}" if obj.usuario else "Sin usuario asignado"
