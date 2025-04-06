from django.contrib import messages
from django.urls import reverse_lazy
# Vistas basadas en clases
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

# Ver lista de empresas
from .models import EmpresaModel
from .forms import EmpresaForm

class EmpresaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'empresa.view_empresamodel'
    model = EmpresaModel
    template_name = 'empresas.html'
    context_object_name = 'empresas'
    paginate_by = 10

class EmpresaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'empresa.view_empresamodel'
    model = EmpresaModel
    template_name = 'empresa_detail.html'
    context_object_name = 'empresa'

class EmpresaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'empresa.delete_empresamodel'
    model = EmpresaModel
    template_name = 'empresa_confirm_delete.html'
    context_object_name = 'empresa'
    success_url = reverse_lazy('empresa_list')
    
    def delete(self, request, *args, **kwargs):
        empresa = self.get_object()
        messages.success(request, f'La empresa "{empresa.razon_social}" ha sido eliminada.')
        return super().delete(request, *args, **kwargs)