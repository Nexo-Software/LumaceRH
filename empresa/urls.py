from django.urls import path, include
from .views import EmpresaListView, EmpresaDetailView, EmpresaWizardView, EmpresaDeleteView, EmpresaUpdateWizardView
from rest_framework.routers import DefaultRouter
from .viewsets import EmpresaViewSet

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)

urlpatterns = [
    path('', EmpresaListView.as_view(), name='empresa_list'),
    path('<int:pk>/', EmpresaDetailView.as_view(), name='empresa_detail'),
    path('create/', EmpresaWizardView.as_view(), name='empresa_create'),
    path('delete/<int:pk>/', EmpresaDeleteView.as_view(), name='empresa_delete'),
    path('update/<int:pk>/', EmpresaUpdateWizardView.as_view(), name='empresa_update'),
    path('api/', include(router.urls)),
]
