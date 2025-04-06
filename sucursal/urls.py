from django.urls import path
from sucursal.views import SucursalListView, SucursalWizardView, SucursalDetailView

urlpatterns = [
    path('', SucursalListView.as_view(), name='sucursal_list'),
    path('nuevo/', SucursalWizardView.as_view(), name='sucursal_create'),
    path('<int:pk>/', SucursalDetailView.as_view(), name='sucursal_detail'),
]
