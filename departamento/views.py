# Django
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
# Vistas
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
# Modelos
from .models import DepartamentoModel
from django.db.models import ProtectedError
# Formularios
from .forms import DepartamentoForm
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class DepartamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'departamento.view_departamentomodel'
    model = DepartamentoModel
    template_name = 'departamentos.html'
    context_object_name = 'departamentos'
    paginate_by = 10
    ordering = ['nombre', 'created_at']

class DepartamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'departamento.add_departamentomodel'
    model = DepartamentoModel
    form_class = DepartamentoForm
    template_name = 'departamento_form.html'
    success_url = reverse_lazy('departamento_list')
    def form_valid(self, form):
        # Asignar el usuario antes de guardar
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class DepartamentoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'departamento.view_departamentomodel'
    model = DepartamentoModel
    template_name = 'departamento_detail.html'
    context_object_name = 'departamento'

class DepartamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'departamento.delete_departamentomodel'
    model = DepartamentoModel
    context_object_name = 'departamento'
    template_name = 'departamento_confirm_delete.html'
    success_url = reverse_lazy('departamento_list')

    def post(self, request, *args, **kwargs):
        departamento = self.get_object()
        try:
            departamento.delete()
            messages.success(request, "Departamento eliminado correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar el departamento porque está relacionado con otros registros.")
        return redirect(self.success_url)