from django import forms
from .models import ContratoModel
from crispy_forms.helper import FormHelper

# Basico
class ContratoBasicForm(forms.ModelForm):
    class Meta:
        model = ContratoModel
        fields = [
            'tipo_contrato',
            'horas_trabajo',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
# Salario
class ContratoSalaryForm(forms.ModelForm):
    class Meta:
        model = ContratoModel
        fields = [
            'salario_base',
            'frecuencia_pago',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
# Fechas
class ContratoDateForm(forms.ModelForm):
    class Meta:
        model = ContratoModel
        fields = [
            'fecha_inicio',
            'fecha_fin',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False