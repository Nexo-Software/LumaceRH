from django.urls import path
from .views import PuestoListView, PuestoCreateView, PuestoDetailView, PuestoDeleteView

urlpatterns = [
    path('', PuestoListView.as_view(), name='puesto_list'),  # Listado de puestos
    path('nuevo/', PuestoCreateView.as_view(), name='puesto_create'),  # Crear nuevo puesto
    path('<int:pk>/', PuestoDetailView.as_view(), name='puesto_detail'),  # Detalle de puesto
    path('eliminar/<int:pk>/', PuestoDeleteView.as_view(), name='puesto_delete'),  # Eliminar puesto
]
