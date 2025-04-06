from django import forms
from .models import EmpresaModel
from crispy_forms.helper import FormHelper

class EmpresaBasicInfoForm(forms.ModelForm):
    class Meta:
        model = EmpresaModel
        fields = ['razon_social', 'nombre_comercial']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class EmpresaAddressForm(forms.ModelForm):
    class Meta:
        model = EmpresaModel
        fields = ['calle', 'numero', 'ciudad', 'codigo_postal', 'provincia', 'pais']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class EmpresaContactForm(forms.ModelForm):
    class Meta:
        model = EmpresaModel
        fields = ['telefono', 'fax', 'email', 'web']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class EmpresaFiscalForm(forms.ModelForm):
    class Meta:
        model = EmpresaModel
        fields = ['rfc']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False