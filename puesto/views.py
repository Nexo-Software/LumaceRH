# Django
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Vistas
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
# Modelos
from .models import PuestoModel
# Formularios
from .forms import PuestoForm
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

class PuestoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'puesto.view_puestomodel'
    model = PuestoModel
    template_name = 'puestos.html'
    context_object_name = 'puestos'
    paginate_by = 10

class PuestoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'puesto.add_puestomodel'    
    model = PuestoModel
    form_class = PuestoForm
    template_name = 'puesto_form.html'
    success_url = reverse_lazy('puesto_list')
    def form_valid(self, form):
        # Asignar el usuario antes de guardar
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)