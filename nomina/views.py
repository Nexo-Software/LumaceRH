from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import UpdateView
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import EmpleadoNominaForm, IncidenciasNominaForm, FechasPagoNominaForm
from .models import NominaModel
from django.shortcuts import redirect, get_object_or_404
from empleado.models import EmpleadoModel
# mensajes de django
from django.contrib import messages


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


class NominaEmpleadoView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    template_name = 'nueva_nomina_wizard.html'
    model = NominaModel
    permission_required = 'nomina.add_empleadomodel'
    form_list = [
        ('fechas_pago', FechasPagoNominaForm),
    ]

    def done(self, form_list, **kwargs):
        pk = self.kwargs.get('pk')
        empleado = get_object_or_404(EmpleadoModel, pk=pk)
        # Incidencias del empleado (incidencias aceptadas)
        incidencias = empleado.incidencias_empleado.filter(estado_incidencia='APROBADA')
        print(f'Empleado: {empleado.postulante.usuario.get_full_name()} - ID: {empleado.id}')
        total_add = 0
        total_sub = 0
        for incidencia in incidencias:
            if incidencia.tipo_incidencia.categoria.efecto == 'ADD':
                print(
                    f'Incidencia: {incidencia.tipo_incidencia.nombre} - Fecha: {incidencia.fecha} - Estado: {incidencia.estado_incidencia} - Monto: {incidencia.monto} - Tipo: {incidencia.tipo_incidencia.categoria.nombre}')
                total_add += incidencia.monto if incidencia.tipo_incidencia.categoria.efecto == 'ADD' else 0
            elif incidencia.tipo_incidencia.categoria.efecto == 'SUB':
                print(
                    f'Incidencia: {incidencia.tipo_incidencia.nombre} - Fecha: {incidencia.fecha} - Estado: {incidencia.estado_incidencia} - Monto: {incidencia.monto} - Tipo: {incidencia.tipo_incidencia.categoria.nombre}')
                total_sub += incidencia.monto if incidencia.tipo_incidencia.categoria.efecto == 'SUB' else 0
        print(f'Total Percepciones: {total_add} - Total Deducciones: {total_sub}')
        # Calcular el total neto
        total_neto = total_add - total_sub
        contrato = empleado.contrato.salario_base * 15
        salario = contrato + total_neto
        print(f'Salario Base: {contrato} - Total Neto: {total_neto} - Salario Final: {salario}')
        formulario = {}
        for form in form_list:
            formulario.update(form.cleaned_data)
        # Campos de auditoria
        formulario['created_by'] = self.request.user
        formulario['updated_by'] = self.request.user
        # Crear la nómina con los datos del formulario
        nomina = NominaModel.objects.create(
            empleado=empleado,
            total_percepciones=total_add,
            total_deducciones=total_sub,
            total_neto=salario,
            **formulario
        )
        # Asignar incidencias a la nómina (many-to-many)
        if incidencias:
            nomina.incidencias.set(incidencias)
        # Guardar la nómina
        try:
            nomina.save()
            messages.success(self.request, 'Nómina guardada exitosamente.')
        except Exception as e:
            print(f'Error al guardar la nómina: {e}')
            messages.error(self.request, 'Error al guardar la nómina. Por favor, inténtelo de nuevo.')
        # Redirigir a una vista de éxito o a la lista de nóminas
        return redirect('test_view')
