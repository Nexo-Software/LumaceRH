from django.urls import reverse_lazy
from django.contrib import messages
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
# Vistas
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Modelos
from .models import SucursalModel
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Formularios
from .forms import SucursalBasicInfoForm, SucursalAddressForm, SucursalContactForm

# Create your views here.
class SucursalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'sucursal.view_sucursalmodel'
    model = SucursalModel
    template_name = 'sucursales.html'
    context_object_name = 'sucursales'
    paginate_by = 10

class SucursalWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'sucursal.add_sucursalmodel'
    template_name = 'sucursal_wizard_form.html'
    form_list = [
        ('basic', SucursalBasicInfoForm),
        ('address', SucursalAddressForm),
        ('contact', SucursalContactForm),
    ]
    
    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)
        
        SucursalModel.objects.create(**form_data)
        return HttpResponseRedirect(reverse_lazy('sucursal_list'))

class SucursalDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'sucursal.view_sucursalmodel'
    model = SucursalModel
    template_name = 'sucursal_detail.html'
    context_object_name = 'sucursal'

class SucursalDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'sucursal.delete_sucursalmodel'
    model = SucursalModel
    context_object_name = 'sucursal'
    template_name = 'sucursal_confirm_delete.html'
    success_url = reverse_lazy('sucursal_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Sucursal eliminada correctamente.")
        return super().delete(request, *args, **kwargs)