from django.urls import path, include
from .views import ContratoListView, ContratoSessionWizarView, ContratoDetailView, ContratoDeleteView
from rest_framework.routers import DefaultRouter
from .viewsets import ContratoViewSet

# Crear un router y registrar el viewset
router = DefaultRouter()
router.register(r'contratos', ContratoViewSet, basename='contrato')

urlpatterns = [
    path('', ContratoListView.as_view(), name='contrato_list'),
    path('nuevo/', ContratoSessionWizarView.as_view(), name='contrato_create'),
    path('<int:pk>/', ContratoDetailView.as_view(), name='contrato_detail'),
    path('delete/<int:pk>/', ContratoDeleteView.as_view(), name='contrato_delete'),
    path('api/', include(router.urls)),
]
