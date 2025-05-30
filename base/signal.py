from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@receiver(user_signed_up)
def enviar_bienvenida(sender, request, user, **kwargs):
    if user.email:
        subject = '¡Bienvenido/a a nuestro sistema!'
        message = f'Hola {user.username}, gracias por registrarte en nuestro sistema.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logger.error(f'Error enviando correo de bienvenida a {user.email}: {e}')