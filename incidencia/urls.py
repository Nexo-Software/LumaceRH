from django.urls import path, include
from .views import EstadoIncidenciaUpdateView, IncidenciasGeneralListView, IncidenciasSucursalListView, IncidenciaUpdateView
urlpatterns = [
    path('actualizar/<int:pk>/', EstadoIncidenciaUpdateView.as_view(), name='estado-incidencia-update'),
    path('incidencias/', IncidenciasGeneralListView.as_view(), name='incidencias-general-list'),
    path('incidencias/sucursal/<int:pk>/', IncidenciasSucursalListView.as_view(), name='incidencias-sucursal-list'),
    path('incidencia/editar/<int:pk>/', IncidenciaUpdateView.as_view(), name='incidencia-update'),
]