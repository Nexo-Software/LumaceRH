# Vistas
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.utils import timezone
# Mensajes
from django.contrib import messages
# Modelos
from .models import IncidenciasEmpleados, ConfiguracionIncidenciasModel
from sucursal.models import SucursalModel
from empleado.models import EmpleadoModel
from horario.models import TurnosModel, SemanaModel, ProgramacionDiariaModel, AsignacionEmpleadoModel
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Shortcuts
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
# Formularios
from .forms import ObservacionesForm
# Timezone
from django.utils import timezone


# Create your views here.

# Modificar incidencias (1x1)
class EstadoIncidenciaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.change_incidenciasempleados'

    def post(self, request, *args, **kwargs):
        incidencia = get_object_or_404(IncidenciasEmpleados, pk=self.kwargs['pk'])  # Obtener la incidencia por ID
        print(f'La incidencia es: {incidencia}')
        estado = request.POST.get('estado')
        print(f'El estado es: {estado}')

        if estado in ['PENDIENTE', 'APROBADA', 'RECHAZADA']:
            incidencia.estado_incidencia = estado
            incidencia.save()
        return redirect(request.META.get('HTTP_REFERER', reverse('dashboard')))


# Modificar incidencias (general)
class EstadoIncdenciasGeneralUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.change_incidenciasempleados'

    def post(self, request, *args, **kwargs):
        incidencias_ids = request.POST.getlist('lista_incidencias')
        accion = request.POST.get('accion')
        # Valida que se haya seleccionado al menos una incidencia
        if not incidencias_ids:
            messages.error(request, 'Debe seleccionar al menos una incidencia.')
            return redirect(request.META.get('HTTP_REFERER', reverse('dashboard')))
        # Obtener todas las incidencias en una sola consulta
        incidencias = IncidenciasEmpleados.objects.filter(id__in=incidencias_ids)

        if accion == 'APROBAR':
            for incidencia in incidencias:
                incidencia.estado_incidencia = 'APROBADA'
                incidencia.save()  # ¡Activa la señal post_save!

        elif accion == 'RECHAZAR':
            for incidencia in incidencias:
                incidencia.estado_incidencia = 'RECHAZADA'
                incidencia.save()  # ¡Activa la señal post_save!
        url = request.POST.get('next')
        if url:
            return redirect(url)
        # Si no se especifica una URL, redirige al dashboard
        return redirect('dashboard')


class IncidenciasGeneralListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.view_incidenciasempleados'
    template_name = 'incidencias_general.html'
    context_object_name = 'incidencias'
    paginate_by = 10

    def get_queryset(self):
        return IncidenciasEmpleados.objects.filter(estado_incidencia='PENDIENTE').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidencias_count'] = self.get_queryset().count()
        context['sucursales'] = SucursalModel.objects.all()
        context['col'] = int(12 / len(context['sucursales']) if context['sucursales'] else 12)
        return context


class IncidenciasSucursalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.view_incidenciasempleados'
    template_name = 'incidencias_sucursal.html'
    context_object_name = 'incidencias'

    # Contexto adicional para la plantilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sucursales'] = SucursalModel.objects.all()
        context['sucursal'] = get_object_or_404(SucursalModel, pk=self.kwargs['pk'])
        context['incidencias_count'] = self.get_queryset().count()
        return context

    # Obtener los empleados de una sucursal específica y de ellos, buscamos sus incidencias
    def get_queryset(self):
        sucursal_id = self.kwargs.get('pk')
        return IncidenciasEmpleados.objects.filter(
            empleado__sucursal_id=sucursal_id,
            estado_incidencia='PENDIENTE'
        ).order_by('-fecha')[:10]  # Limitamos a las 10 últimas incidencias pendientes


class IncidenciaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = IncidenciasEmpleados
    template_name = 'editar_incidencia.html'
    permission_required = 'incidencia.editar_incidencias'
    form_class = ObservacionesForm
    def get_success_url(self):
        # Redirigir a la lista de incidencias del empleado
        # Obtener la url anterior
        if 'next' in self.request.POST:
            return self.request.POST.get('next')
        # Si no hay next, redirigir a la vista de detalle del empleado
        if self.object.empleado:
            # Si la incidencia tiene un empleado asociado, redirigir a su detalle
            return reverse('empleado_detail', kwargs={'pk': self.object.empleado.id})
        # Si no hay empleado asociado, redirigir al dashboard
        return reverse('dashboard')


class IncidencasEmpleadoView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.view_incidenciasempleados'
    template_name = 'historial_incidencias.html'
    context_object_name = 'incidencias'

    def get_queryset(self):
        empleado_id = self.kwargs.get('pk')
        empleado = get_object_or_404(EmpleadoModel, id=empleado_id)
        return IncidenciasEmpleados.objects.filter(empleado=empleado).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empleado'] = get_object_or_404(EmpleadoModel, id=self.kwargs['pk'])
        return context


# Incidencias rapidas para horarios (incidencia a empleados)
class RetardoIncidenciaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.add_incidenciasempleados'
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = get_object_or_404(EmpleadoModel, id=self.kwargs['pk'])
        # Buscar incidencia desde la configuracion de modelo
        # Incidencia que tenga 'TARDANZA'
        tardanza = ConfiguracionIncidenciasModel.objects.filter(tipo_asistencia='TARDANZA').first()
        # Crear la incidencia al empleado
        if tardanza:
            incidencia = IncidenciasEmpleados.objects.create(
                empleado=empleado,
                tipo_incidencia=tardanza.incidencia,
                fecha=timezone.now(),
                estado_incidencia='PENDIENTE',
                observaciones='Retardo registrado automáticamente',
                created_by=self.request.user,
                updated_by=self.request.user
            )
            messages.success(self.request,
                             f'Incidencia de retardo registrada para {empleado.postulante.usuario.get_full_name()} con éxito.')
        else:
            messages.error(self.request, 'No se encontró una configuración de incidencia para tardanzas.')
        return context
    # Redirigir a la lista de incidencias del empleado
    # def get(self, request, *args, **kwargs):
    #    return redirect(reverse('incidencias-empleado-view', kwargs={'pk': self.kwargs['pk']}))


class FaltaIncidenciaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.add_incidenciasempleados'
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = get_object_or_404(EmpleadoModel, id=self.kwargs['pk'])
        # Buscar incidencia desde la configuracion de modelo
        # Incidencia que tenga 'TARDANZA'
        tardanza = ConfiguracionIncidenciasModel.objects.filter(tipo_asistencia='FALTA').first()
        # Crear la incidencia al empleado
        if tardanza:
            incidencia = IncidenciasEmpleados.objects.create(
                empleado=empleado,
                tipo_incidencia=tardanza.incidencia,
                fecha=timezone.now(),
                estado_incidencia='PENDIENTE',
                observaciones='Falta registrada automáticamente',
                created_by=self.request.user,
                updated_by=self.request.user
            )
            # Eliminar al empleado de la programacion diaria
            hora_actual = timezone.now().time()
            # obtener el turno en el que estamos
            turno_actual = TurnosModel.objects.filter(
                hora_inicio__lte=hora_actual,
                hora_fin__gte=hora_actual
            ).first()
            programacion_diaria = ProgramacionDiariaModel.objects.get(
                dia=timezone.now().date(),  # Dia de hoy
                turno=turno_actual
            )
            asignacion = AsignacionEmpleadoModel.objects.filter(
                programacion=programacion_diaria,
                empleado=empleado
            ).first()
            if asignacion:
                print(f'Se encontró la asignación: {asignacion}')
                asignacion.delete()
            messages.success(self.request,
                             f'Incidencia de falta registrada para {empleado.postulante.usuario.get_full_name()} con éxito.')
        else:
            messages.error(self.request, 'No se encontró una configuración de incidencia para tardanzas.')
        return context
