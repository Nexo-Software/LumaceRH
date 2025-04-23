# Señal para que cuando un postulante pase a ser empleado, se cambie el estado del postulante a "Aceptado" y se le asigne el contrato y puesto correspondiente.
from django.db.models.signals import post_save
from .models import PostulanteModel, EmpleadoModel