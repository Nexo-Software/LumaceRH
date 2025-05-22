# Django
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
# Vistas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from formtools.wizard.views import SessionWizardView
# Formularios
from .forms import ContratoBasicForm, ContratoSalaryForm, ContratoDateForm
# Modelos
from .models import ContratoModel
from django.db.models import ProtectedError
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ContratoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ContratoModel # Modelo a utilizar
    template_name = 'contrato_list.html' # Plantilla a utilizar
    context_object_name = 'contratos'
    # constratos = ContratoModel.objects.all()
    permission_required = 'contrato.view_contratomodel'

class ContratoSessionWizarView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'contrato.add_contratomodel'
    template_name = 'contrato_wizard_form.html'
    form_list = [
        ('basic', ContratoBasicForm),
        ('salary', ContratoSalaryForm),
        ('date', ContratoDateForm),
    ]
    
    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)
        # Añadir los campos created_by y updated_by al diccionario form_data
        form_data['created_by'] = self.request.user
        form_data['updated_by'] = self.request.user
        ContratoModel.objects.create(**form_data)
        return HttpResponseRedirect(reverse_lazy('contrato_list'))

class ContratoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ContratoModel # Modelo a utilizar
    template_name = 'contrato_detail.html' # Plantilla a utilizar
    context_object_name = 'contrato'
    permission_required = 'contrato.view_contratomodel'

class ContratoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ContratoModel # Modelo a utilizar
    template_name = 'contrato_confirm_delete.html' # Plantilla a utilizar
    context_object_name = 'contrato'
    success_url = reverse_lazy('contrato_list') # URL a redirigir después de eliminar el objeto
    permission_required = 'contrato.delete_contratomodel'

    def post(self, request, *args, **kwargs):
        contrato = self.get_object()
        try:
            contrato.delete()
            messages.success(request, "Contrato eliminado correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar el contrato porque está relacionado con otros registros.")
        return redirect(self.success_url)
