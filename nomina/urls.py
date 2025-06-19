from django.urls import path
from .views import NuevaNominaWizardView, TestView

urlpatterns = [
    path('generar/', NuevaNominaWizardView.as_view(), name='nueva_nomina_wizard'),
    path('test/', TestView.as_view(), name='test_view'),
]