from django.urls import path
from .views import ContratoListView, ContratoSessionWizarView, ContratoDetailView, ContratoDeleteView

urlpatterns = [
    path('', ContratoListView.as_view(), name='contrato_list'),
    path('nuevo/', ContratoSessionWizarView.as_view(), name='contrato_create'),
    path('<int:pk>/', ContratoDetailView.as_view(), name='contrato_detail'),
    path('delete/<int:pk>/', ContratoDeleteView.as_view(), name='contrato_delete'),
]
