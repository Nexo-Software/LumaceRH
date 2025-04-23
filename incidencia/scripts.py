from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")


from empresa.models import EmpresaModel

empresa = EmpresaModel.objects.first()

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "Eres un asistente de RRHH profesional que debe ayudar a gestionar las incidencias."},
        {"role": "user", "content": f'Los datos de la empresa en mi bd es {empresa}, dime como se llama la emprea (razon social y nombre comercial)'},
    ],
    stream=False
)

respuesta = response.choices[0].message.content