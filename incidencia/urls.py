from django.urls import path, include
from .views import EstadoIncidenciaUpdateView
urlpatterns = [
    path('actualizar/<int:pk>/', EstadoIncidenciaUpdateView.as_view(), name='estado-incidencia-update'),
]
