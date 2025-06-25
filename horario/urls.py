from django.urls import path
from .views import EmpleadosTurnosListView
urlpatterns = [
    path('<int:pk>', EmpleadosTurnosListView.as_view(), name='empleados_turnos_list'),
]