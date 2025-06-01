# Django
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q # Q para consultas complejas
# Vistas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from formtools.wizard.views import SessionWizardView
# Formularios
from .forms import PostulanteInfoForm, PostulanteDireccionForm, PostulantePuestoForm, PostulanteNotasForm, RegistroUsuarioForm, EmpleadoForm, EmpleadoPuestoForm, EmpleadoNotasForm
# Modelos
from .models import PostulanteModel, EmpleadoModel
from django.contrib.auth.models import User
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PostulanteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PostulanteModel # Modelo a utilizar
    template_name = 'postulante_list.html' # Plantilla a utilizar
    context_object_name = 'postulantes'
    permission_required = 'empleado.view_postulante'
    # Modificar el query para que solo mueste a los que estan como pendientes
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(estado='Pendiente')

class NuevoUsuarioView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User # Modelo a utilizar
    form_class = RegistroUsuarioForm # Formulario a utilizar
    template_name = 'nuevo_usuario.html' # Plantilla a utilizar
    success_url = reverse_lazy('postulante_create') # URL de redirección al crear el usuario
    permission_required = 'user.add_postulante'

    def form_valid(self, form):
        # Crear un username
        username = form.cleaned_data['first_name'] + form.cleaned_data['last_name']
        # Limpiar el username
        username = username.replace(" ", "_")
        # Comprobar si el username ya existe
        if User.objects.filter(username=username).exists():
            # Si existe, añadir un número al final
            i = 1
            while User.objects.filter(username=username + str(i)).exists():
                i += 1
            username = username + str(i)
        form.instance.username = username.lower()
        
        # Guardar el usuario
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return super().form_valid(form)

class PostulanteWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'empleado.add_postulante'
    template_name = 'postulante_wizard_form.html'
    form_list = [
        ('info', PostulanteInfoForm),
        ('direccion', PostulanteDireccionForm),
        ('puesto', PostulantePuestoForm),
        ('notas', PostulanteNotasForm),
    ]
    
    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)
        # Añadir los campos created_by y updated_by al diccionario form_data
        form_data['created_by'] = self.request.user
        form_data['updated_by'] = self.request.user
        PostulanteModel.objects.create(**form_data)
        return HttpResponseRedirect(reverse_lazy('postulante_list'))

class PostulanteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = PostulanteModel # Modelo a utilizar
    template_name = 'postulante_detail.html' # Plantilla a utilizar
    context_object_name = 'postulante'
    permission_required = 'empleado.view_postulante'

# Vistas para empleado
class EmpleadoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = EmpleadoModel # Modelo a utilizar
    template_name = 'empleado_list.html' # Plantilla a utilizar
    context_object_name = 'empleados'
    permission_required = 'empleado.view_empleadomodel'

class EmpleadoWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'empleado.add_empleadomodel'
    template_name = 'empleado_wizard_form.html'
    form_list = [
        ('info', EmpleadoForm),
        ('puesto', EmpleadoPuestoForm),
        ('notas', EmpleadoNotasForm),
    ]
    
    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)
        # Añadir los campos created_by y updated_by al diccionario form_data
        form_data['created_by'] = self.request.user
        form_data['updated_by'] = self.request.user
        EmpleadoModel.objects.create(**form_data)
        # Redirigir a la lista de empleados
        return HttpResponseRedirect(reverse_lazy('empleado_list'))

# Buscar empleado por Nombre
class EmpleadoSearchView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = EmpleadoModel
    template_name = 'buscar_empleado.html'
    context_object_name = 'empleados'
    permission_required = 'empleado.view_empleadomodel'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return EmpleadoModel.objects.filter(
                Q(postulante__usuario__first_name__icontains=query) | Q(postulante__usuario__last_name__icontains=query)
            )
        return EmpleadoModel.objects.none()