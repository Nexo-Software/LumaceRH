from django import forms
from .models import PuestoModel
from crispy_forms.helper import FormHelper


class PuestoForm(forms.ModelForm):
    class Meta:
        model = PuestoModel
        fields = ['nombre', 'departamento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False