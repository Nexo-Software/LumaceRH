from django.urls import path
from .views import DepartamentoListView, DepartamentoCreateView, DepartamentoDetailView, DepartamentoDeleteView

urlpatterns = [
    path('', DepartamentoListView.as_view(), name='departamento_list'),
    path('nuevo/', DepartamentoCreateView.as_view(), name='departamento_create'),
    path('<int:pk>/', DepartamentoDetailView.as_view(), name='departamento_detail'),
    path('eliminar/<int:pk>/', DepartamentoDeleteView.as_view(), name='departamento_delete')
]
