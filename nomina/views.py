from django.shortcuts import render
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

class NuevaNominaWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    """
    Vista para crear una nueva nómina utilizando un formulario de varios pasos.
    """
    template_name = 'nueva_nomina_wizard.html'
    form_list = [
        # Aquí se agregarían los formularios necesarios para el proceso de creación de nómina
        # ('step1', Step1Form),
        # ('step2', Step2Form),
        # ...
    ]
    permission_required = 'nomina.add_nomiamodel'

    def done(self, form_list, **kwargs):
        """
        Método que se llama al completar todos los pasos del formulario.
        Aquí se procesan los datos y se crea la nómina.
        """
        # Procesar los datos del formulario y crear la nómina
        return render(self.request, 'nomina/nomina_success.html', {'forms': form_list})