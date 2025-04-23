from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmpleadoModel, PostulanteModel

@receiver(post_save, sender=EmpleadoModel)
def update_postulante_status(sender, instance, created, **kwargs):
    """
    Signal to automatically update postulante status to 'Accepted'
    when a new employee record is created.
    """
    if created:  # Only run when a new record is created, not on updates
        postulante = instance.postulante
        postulante.estado = 'A'  # Set status to "Accepted"
        postulante.save()