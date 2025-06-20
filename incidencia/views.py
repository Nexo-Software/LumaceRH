# Vistas
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
# Modelos
from .models import IncidenciasEmpleados
from sucursal.models import SucursalModel
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Shortcuts
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
# Create your views here.

# Modificar incidencias
class EstadoIncidenciaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.can_manage_incidencia'
    def post(self, request, *args, **kwargs):
        incidencia = get_object_or_404(IncidenciasEmpleados, pk=self.kwargs['pk']) # Obtener la incidencia por ID
        print(f'La incidencia es: {incidencia}')
        estado = request.POST.get('estado')
        print(f'El estado es: {estado}')

        if estado in ['PENDIENTE', 'APROBADA', 'RECHAZADA']:
            incidencia.estado_incidencia = estado
            incidencia.save()
        return redirect(request.META.get('HTTP_REFERER', reverse('dashboard')))

class IncidenciasGeneralListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.can_view_incidencias'
    template_name = 'incidencias_general.html'
    context_object_name = 'incidencias'

    def get_queryset(self):
        return IncidenciasEmpleados.objects.filter(estado_incidencia='PENDIENTE').order_by('-fecha')[:10]  # Limitamos a las 10 últimas incidencias pendientes
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidencias_count'] = self.get_queryset().count()
        context['sucursales'] = SucursalModel.objects.all()
        context['col'] = int(12/len(context['sucursales']) if context['sucursales'] else 12)
        return context

class IncidenciasSucursalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = IncidenciasEmpleados
    permission_required = 'incidencia.can_view_incidencias'
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