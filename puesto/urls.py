from django.urls import path
from .views import PuestoListView, PuestoCreateView

urlpatterns = [
    path('', PuestoListView.as_view(), name='puesto_list'),  # Listado de puestos
    path('nuevo/', PuestoCreateView.as_view(), name='puesto_create'),  # Crear nuevo puesto
]
