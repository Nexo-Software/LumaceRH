from django.urls import path
from .views import NuevaNominaWizardView, TestView, NominaEmpleadoView, ReciboNominaView

urlpatterns = [
    path('generar/', NuevaNominaWizardView.as_view(), name='nueva_nomina_wizard'),
    path('test/', TestView.as_view(), name='test_view'),
    path('empleado/<int:pk>/', NominaEmpleadoView.as_view(), name='nomina_empleado_view'),
    path('recibo/<int:pk>/', ReciboNominaView.as_view(), name='recibo_nomina_view'),
]