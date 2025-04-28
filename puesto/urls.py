from django.urls import path, include
from .views import PuestoListView, PuestoCreateView, PuestoDetailView, PuestoDeleteView
from rest_framework.routers import DefaultRouter
from .viewsets import PuestoViewSet

router = DefaultRouter()
router.register(r'puestos', PuestoViewSet, basename='puesto')

urlpatterns = [
    path('', PuestoListView.as_view(), name='puesto_list'),  # Listado de puestos
    path('nuevo/', PuestoCreateView.as_view(), name='puesto_create'),  # Crear nuevo puesto
    path('<int:pk>/', PuestoDetailView.as_view(), name='puesto_detail'),  # Detalle de puesto
    path('eliminar/<int:pk>/', PuestoDeleteView.as_view(), name='puesto_delete'),  # Eliminar puesto
    path('api/', include(router.urls)),
]
