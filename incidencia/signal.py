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
        - Tipo: {instance.tipo_incidencia.nombre}
        - Categoría: {instance.tipo_incidencia.categoria.nombre}
        - Descripción: '{instance.tipo_incidencia.descripcion}'
        - Sueldo base: {instance.empleado.contrato.salario_base}
        - Horas por turno: {instance.empleado.contrato.horas_trabajo}
        - Diferencia de puesto: {'SÍ' if instance.dif_puesto else 'NO'}

        Instrucciones de cálculo:
        1. SI hay diferencia de puesto ({'SÍ' if instance.dif_puesto else 'NO'}):
           - Usar el monto del contrato diferente: {instance.contrato_obj.salario_base if instance.contrato_obj else 'N/A'}
           - Resultado = Monto del contrato diferente (si está disponible)

        2. SI NO hay diferencia de puesto:
           - Calcular usando sueldo base y descripción:
             * Si la descripción contiene "por hora" o "hora":
                Valor hora = (Sueldo base / 30) / Horas por turno
                Multiplicador = Buscar en descripción porcentaje (ej. '100%' → 1.0, '50%' → 0.5)
                Cantidad = [FALTAN DATOS - devolver 0]
                Resultado = Valor hora * Multiplicador * Cantidad → 0 (sin cantidad)

             * Si la descripción contiene "sueldo base" o equivalente:
                Buscar fracción en descripción (ej. "un sueldo base" → 1, "medio sueldo" → 0.5)
                Resultado = Sueldo base * fracción

             * Otros casos: 0

        3. Reglas absolutas:
           - Solo responder con número (sin formato, símbolos ni texto)
           - Si falta dato esencial → 0
           - Diferencia de puesto tiene prioridad
        """

        # Ejemplo de implementación real sería:
        #   if dif_puesto: return contrato_obj.salario_base
        #   else: parsear descripción para calcular

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
