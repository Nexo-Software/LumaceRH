from django import forms
from .models import ContratoModel
from crispy_forms.helper import FormHelper

# Basico
class ContratoBasicForm(forms.ModelForm):
    class Meta:
        model = ContratoModel
        fields = [
            'nombre',
            'tipo_contrato',
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
            'horas_trabajo',
            'salario_base',
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
        # Formato de fecha
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False