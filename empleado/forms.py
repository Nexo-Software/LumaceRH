from django import forms
from .models import PostulanteModel, EmpleadoModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper

# Registro de Usuario
class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # Hacemos que el campo 'first_name' sea obligatorio.
        # Esto le dirá a Django que no acepte el formulario si este campo está vacío.
        self.fields['first_name'].required = True

        # Hacemos lo mismo para el campo 'last_name'.
        self.fields['last_name'].required = True

        # También podemos cambiar las etiquetas (labels) si queremos que sean más descriptivas
        self.fields['first_name'].label = "Nombre(s)"
        self.fields['last_name'].label = "Apellido(s)"



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
        self.fields['postulante'].queryset = PostulanteModel.objects.filter(estado='Pendiente')
        # Como cambio el contenido del campo 'postulante' para que muestre el nombre del usuario asociado al postulante
        self.fields['postulante'].label_from_instance = lambda obj: f"{obj.usuario.first_name} {obj.usuario.last_name} - {obj.puesto.nombre}" if obj.usuario else "Sin usuario asignado"

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
        # Campos obligatorios
        self.fields['puesto'].required = True
        self.fields['contrato'].required = True
        self.fields['sucursal'].required = True

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