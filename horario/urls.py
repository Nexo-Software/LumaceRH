from django.urls import path
from .views import EmpleadosTurnosListView, ProgramacionDiariaCreateView
urlpatterns = [
    path('<int:pk>', EmpleadosTurnosListView.as_view(), name='empleados_turnos_list'),
    path('nuevo_horario/', ProgramacionDiariaCreateView.as_view(), name='nuevo_horario_test'),
]