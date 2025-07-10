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

# —————— Configuración de Llama v2 ——————
llm = Llama(
    model_path="models/llama-2-7b-chat.Q4_0.gguf",
    n_threads=2
)

# —————— Comandos operativos ——————
comandos = {
    "abrir visual studio":  r'"C:\Users\Gc\AppData\Local\Programs\Microsoft VS Code\Code.exe"',
    "abrir notas":          r"C:\Users\Gc\AppData\Local\Programs\Obsidian\Obsidian.exe",
    "abrir ópera":          r'"C:\Users\Gc\AppData\Local\Programs\Opera GX\opera.exe"',
    "abrir fifa":           r'"C:\Users\Gc\Desktop\FIFA Mod Manager.url"',
    "abrir spotify":        r'start spotify:playlist:6YWYdE2ZE0Wc5KlgdhvAJe',
    "reiniciar cerebro":    None
}

# —————— Inicializar TTS en español ——————
tts = pyttsx3.init()
tts.setProperty('voice',
    'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0'
)
tts.setProperty('rate', 120)
tts.setProperty('volume', 1.0)
# Precalentar para evitar silencio inicial
tts.say("Cerebro 1.0 activado.")
tts.runAndWait()

def hablar(texto: str):
    """Habla de forma sincrónica y lo imprime."""
    print(f"Cerebro: {texto}")
    tts.say(texto)
    tts.runAndWait()

# —————— Precalentar audio ——————
_SD_SR = 16000
try:
    sd.rec(int(0.1 * _SD_SR), samplerate=_SD_SR, channels=1)
    sd.wait()
except:
    pass

# —————— Grabación y reconocimiento ——————
def grabar(duration=3, fs=_SD_SR):
    return sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')

def reconocer(audio_bytes, fs=_SD_SR):
    audio = sr.AudioData(audio_bytes, fs, 2)
    r = sr.Recognizer()
    try:
        return r.recognize_google(audio, language="es-ES").lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        hablar("Error de servicio.")
        return None

# —————— Ejecutar comandos (F9) ——————
def modo_comando():
    hablar("Di tu comando.")
    rec = grabar(duration=3)
    sd.wait()
    cmd = reconocer(rec.tobytes())
    if not cmd:
        hablar("No te entendí.")
        return

    if "reiniciar cerebro" in cmd:
        hablar("Reiniciando Cerebro.")
        os.execl(sys.executable, sys.executable, *sys.argv)

    for key, action in comandos.items():
        if action and key in cmd:
            hablar(f"Ejecutando {key}.")
            subprocess.run(action, shell=True)
            if key == "abrir spotify":
                time.sleep(2)
                ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
                time.sleep(0.1)
                ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            return

    hablar("Comando no reconocido.")

# —————— Modo IA (F10) ——————
def modo_ia():
    hablar("¿Qué quieres preguntarle a la IA?")
    rec = grabar(duration=5)
    sd.wait()
    pregunta = reconocer(rec.tobytes())
    if not pregunta:
        hablar("No entendí tu pregunta.")
        return

    hablar("Pensando…")
    prompt = (
        "Eres un asistente que siempre responde en español.\n"
        f"Usuario: {pregunta}\nIA:"
    )
    salida = llm(prompt, max_tokens=128)
    respuesta = salida['choices'][0]['text'].strip()
    if respuesta:
        hablar(respuesta)
    else:
        hablar("La IA no devolvió respuesta.")

# —————— Bucle principal de escucha de teclas ——————
hablar("Pulsa F9 para comandos o F10 para la IA.")
while True:
    evento = keyboard.read_event()
    if evento.event_type == keyboard.KEY_DOWN:
        if evento.name == "f9":
            modo_comando()
        elif evento.name == "f10":
            modo_ia()
