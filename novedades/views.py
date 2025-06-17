from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class ActualizacionesView(TemplateView):
    template_name = 'actualizacion1.6.html'