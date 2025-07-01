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
        salario_contrario = float(instance.contrato_obj.salario_base) if instance.contrato_obj else 0
        salario_base = float(instance.empleado.contrato.salario_base) if instance.empleado.contrato else 0

        # Asegurar que la diferencia no sea negativa
        dif = max(0, salario_contrario - salario_base)

        print(f'El salario base es: {salario_base}')
        print(f'El salario del contrato contrario es: {salario_contrario}')
        print(f'La diferencia de puesto es: {dif}')

        # Mejorar el prompt con ejemplos concretos de cálculo
        user_prompt = f"""
            Rol: Eres un experto en nóminas mexicano especializado en cálculos de incidencias.
            Datos:
            - Tipo: {instance.tipo_incidencia.nombre}
            - Categoría: {instance.tipo_incidencia.categoria.nombre}
            - Descripción: "{instance.tipo_incidencia.descripcion}"
            - Salario base: ${salario_base:.2f} MXN
            - Horas por turno: {instance.empleado.contrato.horas_trabajo}
            - Diferencia de puesto: {'Sí' if instance.dif_puesto else 'No'} {f'(Valor: ${dif:.2f} MXN)' if instance.dif_puesto else ''}

            Instrucciones:
            1. Si la descripción menciona "horas extras":
               - Calcula: (Salario base / 30 / 8) * Horas extras * 2
            2. Si menciona "día festivo":
               - Calcula: (Salario base / 30) * 3
            3. Si menciona "diferencia de puesto":
               - Añade el valor completo de ${dif:.2f} MXN
            4. Si no hay lógica clara o faltan datos, devuelve 0

            Ejemplos:
            - Descripción: "Pago por 3 horas extras": ({salario_base}/30/8)*3*2
            - Descripción: "Bono por puesto superior": {dif} (si aplica)

            Formato requerido:
            - SOLO EL NÚMERO (sin símbolos, texto o comas)
            - Máximo 2 decimales
            - 0 si no es calculable
            """

        peticion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system",
                 "content": "Eres un calculador de nóminas preciso. Solo devuelve el valor numérico."},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )

        respuesta = peticion.choices[0].message.content

        try:
            # Limpieza robusta de la respuesta
            respuesta_limpia = respuesta.replace("$", "").replace(",", "").replace("MXN", "").strip()
            monto = float(respuesta_limpia)

            # Validación más flexible
            salario_mensual = instance.empleado.contrato.salario_base
            if monto < 0:
                raise ValueError("Monto negativo no permitido")
            if monto > salario_mensual * 5:  # Ampliar rango a 5x el salario
                print(f"Advertencia: Monto elevado pero aceptado: {monto} (Límite anterior: {salario_mensual * 2})")

        except Exception as e:
            print(f"Error en cálculo: {e} | Respuesta original: {respuesta}")
            monto = 0

        print(f"Monto calculado: {monto} ({type(monto)})")
        IncidenciasEmpleados.objects.filter(pk=instance.pk).update(monto=monto)
    elif instance.estado_incidencia == 'RECHAZADA':
        print("La incidencia ha sido rechazada.")
    else:
        print("La incidencia está pendiente de aprobación.")
