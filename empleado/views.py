# Django
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Vistas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from formtools.wizard.views import SessionWizardView
# Formularios
from .forms import PostulanteInfoForm, PostulanteDireccionForm, PostulantePuestoForm, PostulanteNotasForm
# Modelos
from .models import PostulanteModel
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PostulanteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PostulanteModel # Modelo a utilizar
    template_name = 'postulante_list.html' # Plantilla a utilizar
    context_object_name = 'postulantes'
    permission_required = 'empleado.view_postulante'

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