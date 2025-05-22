from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView
# Vistas basadas en clases
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Modelos
from .models import EmpresaModel
from django.db.models import ProtectedError
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Formularios
from .forms import EmpresaBasicInfoForm, EmpresaAddressForm, EmpresaContactForm, EmpresaFiscalForm
# Create your views here.

class EmpresaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'empresa.view_empresamodel'
    model = EmpresaModel
    template_name = 'empresas.html'
    context_object_name = 'empresas'
    paginate_by = 10
    ordering = ['created_at']

class EmpresaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'empresa.view_empresamodel'
    model = EmpresaModel
    template_name = 'empresa_detail.html'
    context_object_name = 'empresa'

class EmpresaWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'empresa.add_empresamodel'
    template_name = 'empresa_wizard_form.html'
    form_list = [
        ('basic', EmpresaBasicInfoForm),
        ('address', EmpresaAddressForm),
        ('contact', EmpresaContactForm),
        ('fiscal', EmpresaFiscalForm),
    ]
    
    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)
        # Añadir los campos created_by y updated_by al diccionario form_data
        form_data['created_by'] = self.request.user
        form_data['updated_by'] = self.request.user
        EmpresaModel.objects.create(**form_data)
        return HttpResponseRedirect(reverse_lazy('empresa_list'))

class EmpresaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'empresa.delete_empresamodel'
    model = EmpresaModel
    template_name = 'empresa_confirm_delete.html'
    context_object_name = 'empresa'
    success_url = reverse_lazy('empresa_list')
    
    def post(self, request, *args, **kwargs):
        empresa = self.get_object()
        try:
            empresa.delete()
            messages.success(request, "Empresa eliminada correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar la empresa porque está relacionada con otros registros.")
        return redirect(self.success_url)

class EmpresaUpdateWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'empresa.change_empresamodel'
    template_name = 'empresa_wizard_form.html'
    form_list = [
        ('basic', EmpresaBasicInfoForm),
        ('address', EmpresaAddressForm),
        ('contact', EmpresaContactForm),
        ('fiscal', EmpresaFiscalForm),
    ]

    def get_form_instance(self, step):
        # Obtener el objeto desde la base de datos solo una vez
        if not hasattr(self, 'empresa'):
            self.empresa = EmpresaModel.objects.get(pk=self.kwargs['pk'])
        return self.empresa

    def done(self, form_list, **kwargs):
        # Guardar el objeto editado
        empresa = self.get_form_instance(None)
        for form in form_list:
            for field, value in form.cleaned_data.items():
                setattr(empresa, field, value)
        empresa.save()
        return redirect('empresa_detail', pk=empresa.pk)
