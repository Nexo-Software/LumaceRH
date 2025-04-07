from django import forms
from .models import DepartamentoModel
from crispy_forms.helper import FormHelper

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = DepartamentoModel
        fields = ['nombre', 'empresa', 'encargado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False