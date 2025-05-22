from django.urls import reverse_lazy
from django.contrib import messages
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
# Vistas
from django.views.generic import ListView, DetailView, DeleteView
# Modelos
from .models import SucursalModel
from django.db.models import ProtectedError
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
    ordering = ['nombre', 'created_at']

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
        form_data['created_by'] = self.request.user
        form_data['updated_by'] = self.request.user
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

    def post(self, request, *args, **kwargs):
        sucursal = self.get_object()
        try:
            sucursal.delete()
            messages.success(request, "Sucursal eliminada correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar la sucursal porque está relacionada con otros registros.")
        return redirect(self.success_url)

class SucursalUpdateWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'sucursal.change_sucursalmodel'
    template_name = 'sucursal_wizard_form.html'
    form_list = [
        ('basic', SucursalBasicInfoForm),
        ('address', SucursalAddressForm),
        ('contact', SucursalContactForm),
    ]

    def get_form_instance(self, step):
        if not hasattr(self, 'sucursal'):
            self.sucursal = SucursalModel.objects.get(pk=self.kwargs['pk'])
        return self.sucursal

    def done(self, form_list, **kwargs):
        # Guardar el objeto editado
        sucursal = self.get_form_instance(None)
        for form in form_list:
            for field, value in form.cleaned_data.items():
                setattr(sucursal, field, value)
        sucursal.save()
        return redirect('sucursal_detail', pk=sucursal.pk)