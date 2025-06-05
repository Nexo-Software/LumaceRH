from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from empleado.models import EmpleadoModel
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from incidencia.models import IncidenciasEmpleados
# Create your views here.

def get_logged_in_users():
    """
    Obtiene una lista de todos los usuarios que tienen una sesión activa.
    """
    # Obtenemos todas las sesiones que no han expirado
    # Las sesiones activas son aquellas cuya fecha de expiración es mayor que la fecha y hora actual.
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    # Creamos una lista para almacenar los IDs de los usuarios
    user_id_list = []

    # Iteramos sobre cada sesión activa
    for session in active_sessions:
        # Obtenemos los datos de la sesión decodificados
        session_data = session.get_decoded()

        # La clave '_auth_user_id' almacena el ID del usuario autenticado en la sesión
        # Si esta clave existe, significa que hay un usuario asociado a esta sesión.
        user_id = session_data.get('_auth_user_id')

        if user_id:
            user_id_list.append(user_id)

    # Eliminamos duplicados si un usuario tiene múltiples sesiones activas
    # y luego obtenemos los objetos User correspondientes a esos IDs.
    # Filtramos por los usuarios cuyos IDs están en nuestra lista.
    logged_in_users = User.objects.filter(id__in=set(user_id_list))

    return logged_in_users
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, **kwargs):
        usuarios = get_logged_in_users()
        context = super().get_context_data(**kwargs)
        context['empleados_count'] = EmpleadoModel.objects.count()
        context['incidencias_count'] = IncidenciasEmpleados.objects.filter(estado_incidencia='PENDIENTE').count()
        context['incidencias'] = IncidenciasEmpleados.objects.filter(estado_incidencia='PENDIENTE').order_by('-fecha')[:5]
        context['logged_in_users'] = usuarios.count()
        return context

class AppView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'apps.html'
    # Permiso : ser administrador (superuser)
    def test_func(self):
        return self.request.user.is_superuser