from .views import ActualizacionesView
from django.urls import path

urlpatterns = [
    path('', ActualizacionesView.as_view(), name='actualizaciones'),
]