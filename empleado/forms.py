from django import forms
from .models import PostulanteModel, EmpleadoModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper

# Registro de Usuario
class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

# Información de Postulante
class PostulanteInfoForm(forms.ModelForm):
    class Meta:
        model = PostulanteModel
        fields = [
            'usuario',
        ]
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


# Empleado Form
# Seleccionar el postulante

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = EmpleadoModel
        fields = [
            'postulante',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class EmpleadoPuestoForm(forms.ModelForm):
    class Meta:
        model = EmpleadoModel
        fields = [
            'puesto',
            'contrato',
            'sucursal',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class EmpleadoNotasForm(forms.ModelForm):
    class Meta:
        model = EmpleadoModel
        fields = [
            'notas', 'fecha_contratacion'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False