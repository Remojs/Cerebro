import sounddevice as sd
import speech_recognition as sr
import pyttsx3
import keyboard
import subprocess
import time
import ctypes
import sys
import os
import winsound             # para el beep en F9
from llama_cpp import Llama
from utils.paths import BASE_USER_PATH
from utils.ia_context import contexto_ia

# —————— Rutas a aplicaciones ——————
VISUAL_STUDIO_PATH = BASE_USER_PATH + r"AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
OBSIDIAN_PATH      = BASE_USER_PATH + r"AppData\\Local\\Programs\\Obsidian\\Obsidian.exe"
OPERA_PATH         = BASE_USER_PATH + r"AppData\\Local\\Programs\\Opera GX\\opera.exe"
FIFA_MANAGER_PATH  = BASE_USER_PATH + r"Desktop\\FIFA Mod Manager.url"
DISCORD_PATH       = BASE_USER_PATH + r"AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe"

# —————— 1) Configuración de Llama v2 ——————
llm = Llama(
    model_path="models/llama-2-7b-chat.Q4_0.gguf",
    n_threads=2,
    verbose=False
)

# —————— 2) Comandos operativos ——————
comandos = {
    "abrir visual studio": f'"{VISUAL_STUDIO_PATH}"',
    "abrir notas":         f'"{OBSIDIAN_PATH}"',
    "abrir ópera":         f'"{OPERA_PATH}"',
    "abrir fifa":          f'"{FIFA_MANAGER_PATH}"',
    "abrir spotify":       'start spotify:playlist:6YWYdE2ZE0Wc5KlgdhvAJe',
    "reiniciar cerebro":   None
}

# —————— 2.1) Modos preconfigurados ——————
modos = {
    "modo juego": [
        r'"C:\\Program Files (x86)\\Steam\\steam.exe"',
        f'"{DISCORD_PATH}"'
    ],
    "modo programación": [
        f'"{VISUAL_STUDIO_PATH}"',
        f'"{OPERA_PATH}"',
        f'"{OBSIDIAN_PATH}"'
    ],
    "modo estudio": [
        f'"{OBSIDIAN_PATH}"',
        f'"{OPERA_PATH}"',
        f'"{DISCORD_PATH}"'
    ]
}

# —————— 3) Inicializar TTS por defecto y voz en español ——————
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 140)
tts_engine.setProperty('volume', 1.0)
# elegir voz en español si está instalada
for v in tts_engine.getProperty('voices'):
    if "spanish" in v.name.lower() or "español" in v.name.lower():
        tts_engine.setProperty('voice', v.id)
        break

def hablar(texto: str):
    """Habla de forma síncrona y lo imprime."""
    print(f"Cerebro: {texto}")
    tts_engine.say(texto)
    tts_engine.runAndWait()

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
        print("Error de servicio de reconocimiento.")
        return None

# —————— 6) Modo Comando (F9) ——————
def modo_comando():
    # beep rápido para indicar “listening”
    winsound.Beep(1000, 150)  # frecuencia 1kHz, duración 150ms

    rec = grabar(2.0)
    sd.wait()
    cmd = reconocer(rec.tobytes())

    if not cmd:
        hablar("No reconocí nada.")
        return

    if "reiniciar cerebro" in cmd:
        hablar("Reiniciando Cerebro.")
        os.execl(sys.executable, sys.executable, *sys.argv)
        return

    for k, action in comandos.items():
        if action and k in cmd:
            hablar(f"Ejecutando {k}.")
            subprocess.run(action, shell=True)
            # forzar play en Spotify
            if k == "abrir spotify":
                time.sleep(2)
                ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
                time.sleep(0.1)
                ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            return

    hablar("Comando no reconocido.")

# —————— 7) Lanzar múltiples apps por modo ——————
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
    hablar("Dime el modo.")
    rec = grabar(2.5)
    sd.wait()
    modo = reconocer(rec.tobytes())
    if not modo:
        hablar("No te escuché bien.")
        return
    modo_multiple(modo)

# —————— 9) Modo IA (F10) ——————
def modo_ia():
    hablar("¿Qué necesitas?")
    rec = grabar(2.5)
    sd.wait()
    pregunta = reconocer(rec.tobytes())
    if not pregunta:
        hablar("No entendí tu pregunta.")
        return

    hablar("Pensando…")
    prompt = contexto_ia + "\nUsuario: " + pregunta + "\nIA:"
    resp = llm(prompt, max_tokens=128)
    texto = resp["choices"][0]["text"].strip()
    if texto:
        hablar(texto)
    else:
        hablar("La IA no devolvió respuesta.")

# —————— 10) Bucle principal ——————
if __name__ == "__main__":
    hablar("Cerebro activado.")
    while True:
        ev = keyboard.read_event()
        if ev.event_type == keyboard.KEY_DOWN:
            if ev.name == "f9":
                modo_comando()
            elif ev.name == "f8":
                modo_por_voz()
            elif ev.name == "f10":
                modo_ia()
