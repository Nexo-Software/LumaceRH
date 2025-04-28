from django.urls import path, include
from .views import DepartamentoListView, DepartamentoCreateView, DepartamentoDetailView, DepartamentoDeleteView
from rest_framework.routers import DefaultRouter
from .viewsets import DepartamentoViewSet

# Crear un router y registrar el ViewSet
router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('', DepartamentoListView.as_view(), name='departamento_list'),
    path('nuevo/', DepartamentoCreateView.as_view(), name='departamento_create'),
    path('<int:pk>/', DepartamentoDetailView.as_view(), name='departamento_detail'),
    path('eliminar/<int:pk>/', DepartamentoDeleteView.as_view(), name='departamento_delete')
]
