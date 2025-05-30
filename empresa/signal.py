from django.db.models.signals import post_save # Despues de crear un registro
from django.dispatch import receiver
from .models import EmpresaModel
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from colorama import Fore
User = get_user_model()

@receiver(post_save, sender=EmpresaModel)
def primeros_pasos(sender, instance, created, **kwargs):
    if created:
        # Enviar un correo de alerta
        print(f"Se ha creado una nueva empresa: {instance.razon_social}")
        destinatarios = list(User.objects.filter(is_active=True).values_list('email', flat=True))
        if destinatarios:
            try:
                send_mail(
                    subject='Nueva Empresa Creada',
                    message=f'La empresa {instance.razon_social} ha sido creada exitosamente.\nEl sistema ha sido configurado correctamente.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=destinatarios,
                    fail_silently=False,
                )
                print(Fore.GREEN + "Notificación por correo electrónico enviada a los usuarios activos.")
            except Exception as e:
                print(Fore.RED + f"Error al enviar la notificación por correo electrónico: {e}")
        else:
            print(Fore.YELLOW + "No hay usuarios activos para enviar la notificación por correo electrónico.")