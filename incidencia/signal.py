from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IncidenciasEmpleados

# IA
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

@receiver(post_save, sender=IncidenciasEmpleados)
def update_postulante_status(sender, instance, created, **kwargs):
    """
    Señal que automatiza el proceso de aprobación de incidencias junto con el monto calculado por IA.
    """
    if created:  # Solo se crea, no se actualiza
        print("La incidencia ha sido creada con éxito.")
    elif instance.estado_incidencia == 'APROBADA':
        print("La incidencia ha sido aprobada.")
        # Hacer que deepseek haga algo con la incidencia
        peticion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un asistente de RRHH profesional  en México del estado de veracruz que debe ayudar a gestionar las incidencias, como respuesta solo quiero que me digas unica y exclusivamente el monto, sin nada de texto."},
                {"role": "user", "content": f'la incidencia aprobada es {instance.tipo_incidencia.nombre}, el sueldo base del empleado es: {instance.empleado.contrato.salario_base} la categoria de la incidencia es: {instance.tipo_incidencia.categoria.nombre} y lo que debes hacer con esta informacion es: {instance.tipo_incidencia.descripcion}'},
            ],
            stream=False
        )

        respuesta = peticion.choices[0].message.content

        respuesta = respuesta.replace("$", "").replace(",", "") # Volver la respuesta a un float
        respuesta = float(respuesta)
        print(respuesta)
        print(type(respuesta))
        IncidenciasEmpleados.objects.filter(pk=instance.pk).update(monto=respuesta)
    elif instance.estado_incidencia == 'RECHAZADA':
        print("La incidencia ha sido rechazada.")
    else:
        print("La incidencia está pendiente de aprobación.")