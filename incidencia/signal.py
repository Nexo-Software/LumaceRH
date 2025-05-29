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

        user_prompt = f"""
        Datos de la incidencia:
        - Tipo de incidencia: {instance.tipo_incidencia.nombre}
        - Categoría: {instance.tipo_incidencia.categoria.nombre}
        - Descripción: {instance.tipo_incidencia.descripcion}
        - Sueldo base del empleado: {instance.empleado.contrato.salario_base}

        Instrucción:
        Calcula el monto a pagar por esta incidencia de forma precisa. Usa el sueldo base y la descripción como referencia.
        Solo responde con el número. No incluyas texto adicional, comas ni símbolos.
        Si no puedes calcularlo, responde 0.
        """

        peticion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system",
                 "content": "Eres un asistente de RRHH profesional en México (Veracruz) que ayuda a calcular el monto exacto a pagar por una incidencia. Solo responde el número."},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )

        respuesta = peticion.choices[0].message.content

        try:
            respuesta = float(respuesta.replace("$", "").replace(",", "").strip())
            if respuesta < 0 or respuesta > instance.empleado.contrato.salario_base * 2:
                raise ValueError("Monto fuera de rango.")
        except Exception as e:
            print("Error al procesar la respuesta de la IA:", e)
            respuesta = 0

        print(respuesta)
        print(type(respuesta))
        IncidenciasEmpleados.objects.filter(pk=instance.pk).update(monto=respuesta)
    elif instance.estado_incidencia == 'RECHAZADA':
        print("La incidencia ha sido rechazada.")
    else:
        print("La incidencia está pendiente de aprobación.")