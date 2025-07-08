import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import keyboard
import subprocess

# ===================== COMANDOS ===================== #
comandos = {
    "abrir visual studio":  r'"C:\Users\Gc\AppData\Local\Programs\Microsoft VS Code\Code.exe"',
    "abrir notas":          r"C:\Users\Gc\AppData\Local\Programs\Obsidian\Obsidian.exe",
    "abrir ópera":          r'"C:\Users\Gc\AppData\Local\Programs\Opera GX\opera.exe"',
    "abrir fifa":           r'"C:\Users\Gc\Desktop\FIFA Mod Manager.url"',
    "reiniciar cerebro":    None
}

# ===================== VOZ ===================== #
tts_engine = pyttsx3.init()
tts_engine.setProperty('voice',
    'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0'
)
tts_engine.setProperty('rate', 120)
tts_engine.setProperty('volume', 1.0)
# 🔥 Pre-calentar TTS
tts_engine.say("")
tts_engine.runAndWait()

def hablar(texto):
    print(f"Cerebro: {texto}")
    tts_engine.say(texto)
    tts_engine.runAndWait()

# ===================== PRE-CALENTAR AUDIO ===================== #
# Graba 0.1 s para que sounddevice abra el stream
_sd_sr = 16000
_sd_ch = 1
try:
    sd.rec(int(0.1 * _sd_sr), samplerate=_sd_sr, channels=_sd_ch)
    sd.wait()
except Exception:
    pass

# ===================== ESCUCHA ===================== #
def escuchar_comando(duration=3, fs=_sd_sr):
    hablar("Di tu comando.")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    audio_data = sr.AudioData(recording.tobytes(), fs, 2)
    r = sr.Recognizer()
    try:
        cmd = r.recognize_google(audio_data, language="es-ES").lower()
        print(f"Escuchado: {cmd}")
        return cmd
    except sr.UnknownValueError:
        hablar("No te entendí.")
    except sr.RequestError:
        hablar("Error de servicio.")
    return None

# ===================== EJECUCIÓN ===================== #
import sys, os
def ejecutar_comando(cmd):
    if cmd and "reiniciar cerebro" in cmd:
        hablar("Reiniciando Cerebro.")
        os.execl(sys.executable, sys.executable, *sys.argv)
        return

    for key, action in comandos.items():
        if action and key in (cmd or ""):
            hablar(f"Ejecutando {key}.")
            subprocess.run(action, shell=True)
            return

    hablar("Comando no reconocido.")

# ===================== INICIO ===================== #
if __name__ == "__main__":
    hablar("Cerebro 1.0 activado.")
    while True:
        if keyboard.is_pressed("F9"):
            cmd = escuchar_comando()
            ejecutar_comando(cmd)
            keyboard.wait("F9")
