# Django
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Vistas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from formtools.wizard.views import SessionWizardView
# Formularios
from .forms import PostulanteForm
# Modelos
from .models import PostulanteModel
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PostulanteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PostulanteModel # Modelo a utilizar
    template_name = 'postulante_list.html' # Plantilla a utilizar
    context_object_name = 'postulantes'
    permission_required = 'empleado.view_postulante'

class PostulanteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PostulanteModel # Modelo a utilizar
    permission_required = 'empleado.add_postulante'
    template_name = 'postulante_form.html' # Plantilla a utilizar
    form_class = PostulanteForm # Formulario a utilizar
    success_url = reverse_lazy('postulante_list') # URL a redirigir al crear el objeto
    def form_valid(self, form):
        # Asignar el usuario antes de guardar
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)