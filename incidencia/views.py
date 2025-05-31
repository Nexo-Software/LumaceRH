# Vistas
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
# Modelos
from .models import IncidenciasEmpleados
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.
