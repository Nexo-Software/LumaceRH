from django import forms
from crispy_forms.helper import FormHelper
from .models import SucursalModel

class SucursalBasicInfoForm(forms.ModelForm):
    class Meta:
        model = SucursalModel
        fields = ['nombre', 'empresa']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class SucursalAddressForm(forms.ModelForm):
    class Meta:
        model = SucursalModel
        fields = ['calle', 'numero', 'ciudad', 'codigo_postal', 'provincia', 'pais']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class SucursalContactForm(forms.ModelForm):
    class Meta:
        model = SucursalModel
        fields = ['telefono', 'fax', 'email', 'web']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False