from django.urls import path, include
from .views import EstadoIncidenciaUpdateView, IncidenciasGeneralListView
urlpatterns = [
    path('actualizar/<int:pk>/', EstadoIncidenciaUpdateView.as_view(), name='estado-incidencia-update'),
    path('incidencias/', IncidenciasGeneralListView.as_view(), name='incidencias-general-list'),
]
