from django.urls import path
from .views import ContratoListView, ContratoSessionWizarView

urlpatterns = [
    path('', ContratoListView.as_view(), name='contrato_list'),
    path('nuevo/', ContratoSessionWizarView.as_view(), name='contrato_create'),
]
