from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import ProgramacionDiariaModel, TurnosModel, SemanaModel, AsignacionEmpleadoModel
from empleado.models import EmpleadoModel
from sucursal.models import SucursalModel
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404

class EmpleadosTurnosListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'horario.view_programaciondiariamodel'
    model = ProgramacionDiariaModel
    template_name = 'empleados_turno.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        # Obtener el turno actual con base a la hora actual
        mi_hora = timezone.now().strftime('%H:%M')
        try:
            turno_actual = TurnosModel.objects.get(
                hora_inicio__lte=mi_hora,
                hora_fin__gte=mi_hora
            )
        except TurnosModel.DoesNotExist:
            messages.error(self.request, "No hay turnos programados para la hora actual.")
            return ProgramacionDiariaModel.objects.none()
        # Obtener la sucursal con el pk
        sucursal = get_object_or_404(SucursalModel, pk=self.kwargs['pk'])
        # Obtener el ultimo registro de la semana de la sucursal
        semana_actual = SemanaModel.objects.filter(
            sucursal=sucursal
        ).order_by('-fecha_inicio').first()
        if not semana_actual:
            messages.error(self.request, "No hay semanas programadas para la sucursal seleccionada.")
            return ProgramacionDiariaModel.objects.none()
        dia_actual = timezone.now().date()
        dia_programado = ProgramacionDiariaModel.objects.get(
            semana=semana_actual,
            dia=dia_actual,
            turno=turno_actual,
        )
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
            hora_fin__gte=mi_hora
        ).first()
        context['turno_actual'] = turno_actual
        return context