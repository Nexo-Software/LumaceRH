from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NomiaModel

# IA
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

@receiver(post_save, sender=NomiaModel)
def update_postulante_status(sender, instance, created, **kwargs):
    if created:  # Only run when a new record is created, not on updates
        print("Nomina creada con exito.")
    elif instance.estado_nomina == 'GENERADA':
        # Obtener las incidencias
        incidencias = instance.incidencias.all()
        total_deducciones = 0
        total_percepciones = 0
        total_neto = 0
        # Recorrer las incidencias y calcular el total
        for incidencia in incidencias:
            print(incidencia.tipo_incidencia.categoria.efecto) # ADD (PERSERPCION) o SUB (DEDUCCION)
            if incidencia.tipo_incidencia.categoria.efecto == 'ADD':
                total_percepciones += incidencia.monto
            elif incidencia.tipo_incidencia.categoria.efecto == 'SUB':
                total_deducciones += incidencia.monto
        print(f'Los totales son:\nPersepciones: ${total_percepciones}\nDeducciones: ${total_deducciones}')
        # Calcular el total neto
        total_neto = total_percepciones - total_deducciones
        salario = total_neto + (instance.empleado.contrato.salario_base * 15)
        print(f'El salario de neto: {salario}')
        NomiaModel.objects.filter(pk=instance.pk).update(
            total_percepciones=total_percepciones,
            total_deducciones=total_deducciones,
            total_neto=salario,
        )
        #print("Incidencias: ", incidencias)
        print("La nomina a sido calculada y generada ha sido generada.")
