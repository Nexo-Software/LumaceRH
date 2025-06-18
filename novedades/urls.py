from .views import ActualizacionesView, NovedadesView
from django.urls import path

urlpatterns = [
    path('', ActualizacionesView.as_view(), name='actualizaciones'),
    path('novedades/', NovedadesView.as_view(), name='novedades'),
]
