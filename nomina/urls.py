from django.urls import path
from .views import NuevaNominaWizardView, TestView, NominaEmpleadoView

urlpatterns = [
    path('generar/', NuevaNominaWizardView.as_view(), name='nueva_nomina_wizard'),
    path('test/', TestView.as_view(), name='test_view'),
    path('empleado/<int:pk>/', NominaEmpleadoView.as_view(), name='nomina_empleado_view'),
]