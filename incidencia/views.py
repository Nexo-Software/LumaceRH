# Vistas
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
# Modelos
from .models import IncidenciasEmpleados
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
