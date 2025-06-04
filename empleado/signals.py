from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmpleadoModel, PostulanteModel
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Generar contraseña aleatoria
from secure_password_generator_ikac import generar_contrasena
from django.conf import settings

@receiver(post_save, sender=EmpleadoModel)
def update_postulante_status(sender, instance, created, **kwargs):
    """
    Signal to automatically update postulante status to 'Accepted'
    when a new employee record is created.
    """
    if created:  # Only run when a new record is created, not on updates
        postulante = instance.postulante
        postulante.estado = 'Aceptado'  # Set status to "Accepted"
        postulante.save()
        # Crear una contraseña a su usuario y mandarla por correo
        new_password = generar_contrasena()
        postulante.usuario.set_password(new_password)
        postulante.usuario.save()
        # Enviar correo al postulante con la nueva contraseña
        subject = f'Hola {postulante.usuario.first_name}, tu cuenta ha sido activada'
        message = f'Hola {postulante.usuario.first_name},\n\nTu cuenta ha sido activada y puedes iniciar sesión con la siguiente contraseña:\n\n{new_password}\n\nPor favor, cambia tu contraseña al iniciar sesión por primera vez.\n\nSaludos,\nEl equipo de Recursos Humanos'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [postulante.usuario.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            # Manejo de errores al enviar el correo
            print(f'Error al enviar el correo: {e}')

