from django import forms
from .models import PostulanteModel
from crispy_forms.helper import FormHelper
from django_select2 import forms as s2forms

class AuthorWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "username__icontains",
        "email__icontains",
    ]

# Información de Postulante
class PostulanteInfoForm(forms.ModelForm):
    class Meta:
        model = PostulanteModel
        fields = [
            'usuario',
        ]
        widgets = {
            'usuario': AuthorWidget()
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class PostulanteDireccionForm(forms.ModelForm):
    class Meta:
        model = PostulanteModel
        fields = [
            'calle',
            'numero',
            'ciudad',
            'codigo_postal',
            'provincia',
            'pais',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class PostulantePuestoForm(forms.ModelForm):
    class Meta:
        model = PostulanteModel
        fields = [
            'puesto',
            'contrato',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class PostulanteNotasForm(forms.ModelForm):
    class Meta:
        model = PostulanteModel
        fields = [
            'notas',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

