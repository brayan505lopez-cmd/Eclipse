import os
import asyncio
import edge_tts
from groq import Groq
import pygame

os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

pygame.mixer.init()

try:
    with open("alma.txt", "r", encoding="utf-8") as f:
        alma = f.read()
except:
    alma = "Eres Eclipse, el asistente personal de Brayan. Le tratas de usted."

def hablar(texto):
    async def _generar():
        voz = "es-MX-JorgeNeural" 
        texto_limpio = texto.replace('*', '').replace('#', '')
        communicate = edge_tts.Communicate(texto_limpio, voz)
        await communicate.save("voz_pc.mp3")
        
        pygame.mixer.music.load("voz_pc.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    asyncio.run(_generar())

print("\n🌑 Eclipse en PC. Escriba 'salir' para terminar.\n")

while True:
    consulta = input("Brayan: ")
    if consulta.lower() in ['salir', 'exit', 'quit']:
        break
        
    print("[🧠 Pensando...]")
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b", 
            messages=[
                {"role": "system", "content": alma + "\n\nResponde solo a este mensaje."},
                {"role": "user", "content": consulta}
            ]
        )
        respuesta = completion.choices[0].message.content
        print(f"Eclipse: {respuesta}\n")
        hablar(respuesta)
    except Exception as e:
        print(f"Error: {e}")
