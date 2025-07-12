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
from paths import BASE_USER_PATH

# Construcción de rutas específicas
VISUAL_STUDIO_PATH = BASE_USER_PATH + r"AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
OBSIDIAN_PATH = BASE_USER_PATH + r"AppData\\Local\\Programs\\Obsidian\\Obsidian.exe"
OPERA_PATH = BASE_USER_PATH + r"AppData\\Local\\Programs\\Opera GX\\opera.exe"
FIFA_MANAGER_PATH = BASE_USER_PATH + r"Desktop\\FIFA Mod Manager.url"
DISCORD_PATH = BASE_USER_PATH + r"AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe"

# —————— 1) Configuración de Llama v2 (silencioso) ——————
llm = Llama(
    model_path="models/llama-2-7b-chat.Q4_0.gguf",
    n_threads=2,
    verbose=False
)

# —————— 2) Lista de comandos operativos ——————
comandos = {
    "abrir visual studio": f'"{VISUAL_STUDIO_PATH}"',
    "abrir notas": f'"{OBSIDIAN_PATH}"',
    "abrir ópera": f'"{OPERA_PATH}"',
    "abrir fifa": f'"{FIFA_MANAGER_PATH}"',
    "abrir spotify": 'start spotify:playlist:6YWYdE2ZE0Wc5KlgdhvAJe',
    "reiniciar cerebro": None
}

# —————— 2.1) Definición de modos preconfigurados ——————
modos = {
    "juego": [
        r'"C:\\Program Files (x86)\\Steam\\steam.exe"',
        f'"{DISCORD_PATH}"'
    ],
    "programación": [
        f'"{VISUAL_STUDIO_PATH}"',
        f'"{OPERA_PATH}"',
        f'"{OBSIDIAN_PATH}"'
    ],
    "estudio": [
        f'"{OBSIDIAN_PATH}"',
        f'"{OPERA_PATH}"',
        f'"{DISCORD_PATH}"'
    ]
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
    hablar("Di tu comando.")
    rec = grabar(2.5); sd.wait()
    cmd = reconocer(rec.tobytes())
    if not cmd:
        hablar("No se reconoció ningún comando.")
        return

    print(f"Comando reconocido: {cmd}")
    if "reiniciar cerebro" in cmd:
        hablar("Reiniciando Cerebro.")
        os.execl(sys.executable, sys.executable, *sys.argv)
        return

    for k, action in comandos.items():
        if action and k in cmd:
            hablar(f"Ejecutando {k}.")
            subprocess.run(action, shell=True)
            if k == "abrir spotify":
                time.sleep(2)
                ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
                time.sleep(0.1)
                ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            return

    hablar("Comando no reconocido.")

# —————— 7) Función para lanzar múltiples apps (modos) ——————
def modo_multiple(nombre: str):
    apps = modos.get(nombre, [])
    if not apps:
        hablar(f"No existe el modo «{nombre}».")
        return
    hablar(f"Iniciando modo {nombre}.")
    for ruta in apps:
        subprocess.Popen(ruta, shell=True)
        time.sleep(1)
    hablar(f"Modo {nombre} listo.")

# —————— 8) Selección de modo por voz (F8) ——————
def modo_por_voz():
    hablar("Dime el modo que quieres activar.")
    rec = grabar(3); sd.wait()
    modo = reconocer(rec.tobytes())
    if not modo:
        hablar("No te escuché bien.")
        return
    modo = modo.lower()
    modo_multiple(modo)

# —————— 9) Modo IA (F10) ——————
def modo_ia():
    hablar("¿Qué necesitas?")
    rec = grabar(2); sd.wait()
    pregunta = reconocer(rec.tobytes())
    if not pregunta:
        hablar("No entendí tu pregunta.")
        return

    print(f"Procesando pregunta: {pregunta}")
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

# —————— 10) Bucle de teclas con modos ——————
hablar("Cerebro Activado. F9=comandos, F10=IA, F8=activar modo por voz.")
while True:
    ev = keyboard.read_event()
    if ev.event_type == keyboard.KEY_DOWN:
        if ev.name == "f9":
            modo_comando()
        elif ev.name == "f10":
            modo_ia()
        elif ev.name == "f8":
            modo_por_voz()
