from django.urls import path
from .views import EmpresaListView, EmpresaDetailView, EmpresaWizardView, EmpresaDeleteView

urlpatterns = [
    path('', EmpresaListView.as_view(), name='empresa_list'),
    path('<int:pk>/', EmpresaDetailView.as_view(), name='empresa_detail'),
    path('create/', EmpresaWizardView.as_view(), name='empresa_create'),
    path('delete/<int:pk>/', EmpresaDeleteView.as_view(), name='empresa_delete')
]
