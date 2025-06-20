from django.forms import ModelForm
from .models import IncidenciasEmpleados
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Submit, Field, HTML


class ObservacionesForm(ModelForm):
    class Meta:
        model = IncidenciasEmpleados
        fields = ['observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Verifica si hay una instancia y muestra su valor

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar', css_class='btn-primary'))
