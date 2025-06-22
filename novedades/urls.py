from .views import ActualizacionesView, NovedadesView, NovedadesView2
from django.urls import path

urlpatterns = [
    path('', ActualizacionesView.as_view(), name='actualizaciones'),
    path('novedades/', NovedadesView.as_view(), name='novedades'),
    path('proximo/', NovedadesView2.as_view(), name='novedades2'),
]
