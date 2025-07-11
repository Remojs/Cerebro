import sounddevice as sd
import speech_recognition as sr
import pyttsx3
import keyboard
import subprocess
import time
import ctypes
import sys
import os
from llama_cpp import Llama

# —————— 1) Configuración de Llama v2 (silencioso) ——————
llm = Llama(
    model_path="models/llama-2-7b-chat.Q4_0.gguf",
    n_threads=2,
    verbose=False
)

# —————— 2) Lista de comandos operativos ——————
comandos = {
    "abrir visual studio": r'"C:\Users\Gc\AppData\Local\Programs\Microsoft VS Code\Code.exe"',
    "abrir notas":         r"C:\Users\Gc\AppData\Local\Programs\Obsidian\Obsidian.exe",
    "abrir ópera":         r'"C:\Users\Gc\AppData\Local\Programs\Opera GX\opera.exe"',
    "abrir fifa":          r'"C:\Users\Gc\Desktop\FIFA Mod Manager.url"',
    "abrir spotify":       r'start spotify:playlist:6YWYdE2ZE0Wc5KlgdhvAJe',
        "abrir spotify":       r'start spotify:playlist:6YWYdE2ZE0Wc5KlgdhvAJe',
    "reiniciar cerebro":   None
}

# —————— 3) Funciones de TTS ——————
def listar_voces():
    engine = pyttsx3.init()
    return engine.getProperty('voices')

def hablar(texto: str):
    print(f"Cerebro: {texto}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        for voice in engine.getProperty('voices'):
            if "spanish" in voice.name.lower() or "español" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(texto)
        engine.runAndWait()
    except Exception as e:
        print(f"Error de voz: {e}")

# Diagnóstico inicial de voces
try:
    voces = listar_voces()
    print(f"Voces disponibles: {len(voces)}")
    if voces:
        print(f"Primera voz: {voces[0].name}")
except:
    print("No se pudieron listar las voces")
print("Iniciando asistente...")

# —————— 4) Precalentar audio micro ——————
_SR = 16000
try:
    sd.rec(int(0.1 * _SR), samplerate=_SR, channels=1)
    sd.wait()
except:
    pass

# —————— 5) Grabación y reconocimiento ——————
def grabar(segundos=2.5):
    return sd.rec(int(segundos * _SR), samplerate=_SR, channels=1, dtype='int16')

def reconocer(audio_bytes):
    audio = sr.AudioData(audio_bytes, _SR, 2)
    recog = sr.Recognizer()
    try:
        return recog.recognize_google(audio, language="es-ES").lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        print("Error de servicio de reconocimiento de voz.")
        return None

# —————— 6) Modo Comando (F9) ——————
def modo_comando():
    print("Escuchando comando...")
    rec = grabar(2.5); sd.wait()
    cmd = reconocer(rec.tobytes())
    if not cmd:
        print("No se reconoció ningún comando")
        return

    print(f"Comando reconocido: {cmd}")
    if "reiniciar cerebro" in cmd:
        print("Reiniciando Cerebro.")
        os.execl(sys.executable, sys.executable, *sys.argv)
        return

    for k, action in comandos.items():
        if action and k in cmd:
            print(f"Ejecutando: {k}")
            subprocess.run(action, shell=True)
            if k == "abrir spotify":
                time.sleep(2)
                ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
                time.sleep(0.1)
                ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            return

    print("Comando no reconocido.")

# —————— 7) Modo IA (F10) ——————
def modo_ia():
    hablar("¿Qué necesitas?")
    rec = grabar(2); sd.wait()
    pregunta = reconocer(rec.tobytes())
    if not pregunta:
        hablar("No entendí tu pregunta.")
        return

    print(f"Procesando pregunta: {pregunta}")
    
    # Flujo normal de IA
    hablar("Pensando…")
    prompt = (
        "Eres un asistente experto que siempre RESPONDE en español.\n"
        f"Usuario: {pregunta}\nIA:"
    )
    resp = llm(prompt, max_tokens=128)
    texto = resp["choices"][0]["text"].strip()
    if texto:
        print(f"Respuesta IA: {texto}")
        hablar(texto)
    else:
        hablar("La IA no devolvió respuesta.")
# —————— 8) Bucle de teclas ——————
hablar("Cerebro Activado")
while True:
    ev = keyboard.read_event()
    if ev.event_type == keyboard.KEY_DOWN:
        if ev.name == "f9":
            modo_comando()
        elif ev.name == "f10":
            modo_ia()
