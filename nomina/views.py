from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import UpdateView
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import EmpleadoNominaForm, IncidenciasNominaForm, FechasPagoNominaForm
from .models import NominaModel
from django.shortcuts import redirect, get_object_or_404
from empleado.models import EmpleadoModel
import datetime
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
        formulario = {}
        for form in form_list:
            formulario.update(form.cleaned_data)
        # fecha de inicio y fin
        fecha_inicio = formulario.get('fecha_inicio')
        fecha_fin = formulario.get('fecha_fin')
        pk = self.kwargs.get('pk')
        empleado = get_object_or_404(EmpleadoModel, pk=pk)
        # Incidencias del empleado (incidencias aceptadas y que esten dentro del rango de fechas)
        # Nuscar si hay incidencias pendientes del empleado (si las hay no se puede generar la nómina)
        if empleado.incidencias_empleado.filter(estado_incidencia='PENDIENTE', fecha__range=(fecha_inicio,fecha_fin)).exists():
            messages.error(self.request, 'El empleado tiene incidencias pendientes. No se puede generar la nómina.')
            return redirect('empleado_detail', pk=empleado.id)
        incidencias = empleado.incidencias_empleado.filter(estado_incidencia='APROBADA', fecha__range=(fecha_inicio, fecha_fin))
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
        # Buscar nomina con la misma fecha de generacion y empleado
        fecha_actual = datetime.date.today()
        nomina_existente = NominaModel.objects.filter(empleado=empleado, fecha_generacion=fecha_actual).first()
        if nomina_existente:
            messages.warning(self.request, 'Ya existe una nómina generada para este empleado en esta fecha.')
            return redirect('recibo_nomina_view', pk=empleado.id)
        # Si la nomina no existe, se guarda la nueva nómina
        try:
            nomina.save()
            messages.success(self.request, 'Nómina guardada exitosamente.')
        except Exception as e:
            print(f'Error al guardar la nómina: {e}')
            messages.error(self.request, 'Error al guardar la nómina. Por favor, inténtelo de nuevo.')
        # Redirigir a una vista de éxito o a la lista de nóminas
        return redirect('recibo_nomina_view', pk=empleado.id) # redirigir a la vista del recibo de nómina del empleado (ultima nomina)

class ReciboNominaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView): #Obtener la ultima nómina del empleado
    """
    Vista para generar un recibo de nómina.
    """
    template_name = 'recibo_nomina.html'
    permission_required = 'nomina.view_nomiamodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        empleado = get_object_or_404(EmpleadoModel, pk=pk)
        context['empleado'] = empleado
        nomina = NominaModel.objects.filter(empleado=empleado).latest('fecha_generacion')
        context['nomina'] = nomina
        return context
