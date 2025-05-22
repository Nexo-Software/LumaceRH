from django.urls import path, include
from sucursal.views import SucursalListView, SucursalWizardView, SucursalDetailView, SucursalDeleteView, SucursalUpdateWizardView
from rest_framework.routers import DefaultRouter
from .viewsets import SucursalViewSet
# Crear un router y registrar el ViewSet
router = DefaultRouter()
router.register(r'sucursales', SucursalViewSet)

urlpatterns = [
    path('', SucursalListView.as_view(), name='sucursal_list'),
    path('nuevo/', SucursalWizardView.as_view(), name='sucursal_create'),
    path('<int:pk>/', SucursalDetailView.as_view(), name='sucursal_detail'),
    path('delete/<int:pk>/', SucursalDeleteView.as_view(), name='sucursal_delete'),
    path('update/<int:pk>/', SucursalUpdateWizardView.as_view(), name='sucursal_update'),
    path('api/', include(router.urls))
]