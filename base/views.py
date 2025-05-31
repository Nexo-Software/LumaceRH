from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from empleado.models import EmpleadoModel
from incidencia.models import IncidenciasEmpleados
# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empleados_count'] = EmpleadoModel.objects.count()
        context['incidencias_count'] = IncidenciasEmpleados.objects.filter(estado_incidencia='PENDIENTE').count()
        context['incidencias'] = IncidenciasEmpleados.objects.filter(estado_incidencia='PENDIENTE').order_by('-fecha')[:5]
        return context

class AppView(LoginRequiredMixin, TemplateView):
    template_name = 'apps.html'