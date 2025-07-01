from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import ProgramacionDiariaModel, TurnosModel, SemanaModel, AsignacionEmpleadoModel
from empleado.models import PostulanteModel, EmpleadoModel
from .forms import AsignacionEmpleadoFormSet
from empleado.models import EmpleadoModel
from sucursal.models import SucursalModel
from incidencia.models import IncidenciasEmpleados, TipoIncidenciasModel
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


class EmpleadosTurnosListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'horario.view_programaciondiariamodel'
    model = ProgramacionDiariaModel
    template_name = 'empleados_turno.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        # Obtener el turno actual con base a la hora actual
        mi_hora = timezone.now().strftime('%H:%M')
        sucursal = get_object_or_404(SucursalModel, pk=self.kwargs['pk'])
        try:
            turno_actual = TurnosModel.objects.get(
                hora_inicio__lte=mi_hora,
                hora_fin__gte=mi_hora,
                sucursal = sucursal
            )
        except TurnosModel.DoesNotExist:
            messages.error(self.request, f'No hay turnos programados para la hora actual. ({mi_hora})')
            return ProgramacionDiariaModel.objects.none()
        # Obtener el ultimo registro de la semana de la sucursal
        semana_actual = SemanaModel.objects.filter(
            sucursal=sucursal
        ).order_by('-fecha_inicio').first()
        if not semana_actual:
            messages.error(self.request, "No hay semanas programadas para la sucursal seleccionada.")
            return ProgramacionDiariaModel.objects.none()
        dia_actual = timezone.now().date()
        try:
            dia_programado = ProgramacionDiariaModel.objects.get(
                semana=semana_actual,
                dia=dia_actual,
                turno=turno_actual,
            )
        except ProgramacionDiariaModel.DoesNotExist:
            messages.error(self.request, f"No hay programación para el día {dia_actual} en el turno actual.")
            return ProgramacionDiariaModel.objects.none()
        # Obtener los empleados del dia_programado
        empleados = AsignacionEmpleadoModel.objects.filter(
            programacion=dia_programado
        ).select_related('empleado').values_list('empleado__id', flat=True)
        empleados = list(empleados)
        find_empleados = EmpleadoModel.objects.filter(id__in=empleados)
        if not find_empleados.exists():
            messages.warning(self.request, "No hay empleados asignados para el turno actual.")
            return ProgramacionDiariaModel.objects.none()
        return find_empleados

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener la sucursal con el pk
        sucursal = get_object_or_404(SucursalModel, pk=self.kwargs['pk'])
        context['sucursal'] = sucursal
        # Obtener el turno actual con base a la hora actual
        mi_hora = timezone.now().strftime('%H:%M')
        turno_actual = TurnosModel.objects.filter(
            hora_inicio__lte=mi_hora,
            hora_fin__gte=mi_hora,
            sucursal = sucursal
        ).first()
        print(f'El turno actual es: {turno_actual}')
        context['turno_actual'] = turno_actual
        return context


class ProgramacionDiariaCreateView(CreateView):
    model = ProgramacionDiariaModel
    form_class = AsignacionEmpleadoFormSet
    template_name = 'crear_horario.html'
    success_url = reverse_lazy('lista_programaciones')  # Ajusta con tu URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AsignacionEmpleadoFormSet(self.request.POST, prefix='empleados')
        else:
            context['formset'] = AsignacionEmpleadoFormSet(prefix='empleados')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Asignar usuario creador
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.updated_by = self.request.user
            self.object.save()

            # Guardar formset
            formset.instance = self.object
            instances = formset.save(commit=False)
            for instance in instances:
                instance.created_by = self.request.user
                instance.updated_by = self.request.user
                instance.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProgramacionDiariaUpdateView(UpdateView):
    model = ProgramacionDiariaModel
    form_class = AsignacionEmpleadoFormSet
    template_name = 'crear_horario.html'
    success_url = reverse_lazy('lista_programaciones')  # Ajusta con tu URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AsignacionEmpleadoFormSet(
                self.request.POST,
                instance=self.object,
                prefix='empleados'
            )
        else:
            context['formset'] = AsignacionEmpleadoFormSet(
                instance=self.object,
                prefix='empleados'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Asignar usuario actualizador
            self.object = form.save(commit=False)
            self.object.updated_by = self.request.user
            self.object.save()

            # Guardar formset
            instances = formset.save(commit=False)
            for instance in instances:
                # Solo para nuevas instancias
                if not instance.pk:
                    instance.created_by = self.request.user
                instance.updated_by = self.request.user
                instance.save()

            # Eliminar marcados para borrar
            for obj in formset.deleted_objects:
                obj.delete()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
