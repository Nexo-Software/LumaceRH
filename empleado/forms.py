from django import forms
from .models import PostulanteModel
from crispy_forms.helper import FormHelper

class PostulanteForm(forms.ModelForm):
    class Meta:
        model = PostulanteModel
        fields = [
            'usuario',
            'puesto',
            'contrato',
            'notas',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

