from django.shortcuts import render
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import EmpleadoNominaForm, IncidenciasNominaForm, FechasPagoNominaForm
from .models import NominaModel
from django.shortcuts import redirect
from empleado.models import EmpleadoModel


# Create your views here.

class TestView(LoginRequiredMixin, TemplateView):
    """
    Vista de prueba para verificar el funcionamiento del sistema.
    """
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = '¡Esta es una vista de prueba!'
        return context


class NuevaNominaWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    """
    Vista para crear una nueva nómina utilizando un formulario de varios pasos.
    """
    template_name = 'nueva_nomina_wizard.html'
    form_list = [
        ('empleado', EmpleadoNominaForm),
        ('fechas_pago', FechasPagoNominaForm),
        ('incidencias', IncidenciasNominaForm),
    ]
    permission_required = 'nomina.add_nomiamodel'

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        # Solo para el paso de incidencias
        if step == 'incidencias':
            # Obtener datos del paso 'empleado'
            empleado_data = self.get_cleaned_data_for_step('empleado')
            if empleado_data:
                empleado = empleado_data.get('empleado')
                kwargs['empleado'] = empleado

        return kwargs

    def done(self, form_list, **kwargs):
        formulario = {}
        incidencias = None
        for form in form_list:
            formulario.update(form.cleaned_data)
            if 'incidencias' in form.cleaned_data:
                incidencias = form.cleaned_data['incidencias']
        # Paso 2: Eliminar el campo 'incidencias' del diccionario principal
        if 'incidencias' in formulario:
            del formulario['incidencias']
        # Campos de auditoria
        formulario['created_by'] = self.request.user
        formulario['updated_by'] = self.request.user
        # Crear la nómina con los datos del formulario
        # Paso 4: Crear la instancia de NominaModel SIN las incidencias
        nomina = NominaModel.objects.create(**formulario)

        # Paso 5: Asignar incidencias usando .set() si existen
        if incidencias:
            nomina.incidencias.set(incidencias)
        # Cambiar el estado de la nómina a 'GENERADA'
        nomina.estado_nomina = 'GENERADA'
        nomina.save()
        # Redirigir a una vista de éxito o a la lista de nóminas
        return redirect('test_view')


class NominaEmpleadoView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'nueva_nomina_wizard.html'
    form_list = [
        ('fechas_pago', FechasPagoNominaForm),
        ('incidencias', IncidenciasNominaForm),
    ]
    permission_required = 'nomina.add_nomiamodel'

    def get_form_instance(self, step):
        # Obtener el objeto desde la base de datos solo una vez
        if not hasattr(self, 'empleado'):
            self.empleado = EmpleadoModel.objects.get(pk=self.kwargs['pk'])
        return self.empleado

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        # Solo para el paso de incidencias
        if step == 'incidencias':
            # Obtener datos del paso 'empleado'
            empleado_data = self.get_cleaned_data_for_step('empleado')
            if empleado_data:
                empleado = empleado_data.get('empleado')
                kwargs['empleado'] = empleado
        return kwargs

    def done(self, form_list, **kwargs):
        formulario = {}
        incidencias = None
        for form in form_list:
            formulario.update(form.cleaned_data)
            if 'incidencias' in form.cleaned_data:
                incidencias = form.cleaned_data['incidencias']
        # Paso 2: Eliminar el campo 'incidencias' del diccionario principal
        if 'incidencias' in formulario:
            del formulario['incidencias']
        # Campos de auditoria
        formulario['created_by'] = self.request.user
        formulario['updated_by'] = self.request.user
        # Crear la nómina con los datos del formulario
        # Paso 4: Crear la instancia de NominaModel SIN las incidencias
        nomina = NominaModel.objects.create(**formulario)

        # Paso 5: Asignar incidencias usando .set() si existen
        if incidencias:
            nomina.incidencias.set(incidencias)
        # Cambiar el estado de la nómina a 'GENERADA'
        nomina.estado_nomina = 'GENERADA'
        nomina.save()
        # Redirigir a una vista de éxito o a la lista de nóminas
        return redirect('test_view')
