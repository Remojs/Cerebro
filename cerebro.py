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
    verbose=False  # <— aquí silenciamos los logs de repack
)

# —————— 2) Lista de comandos operativos ——————
comandos = {
    "abrir visual studio":  r'"C:\Users\Gc\AppData\Local\Programs\Microsoft VS Code\Code.exe"',
    "abrir notas":          r"C:\Users\Gc\AppData\Local\Programs\Obsidian\Obsidian.exe",
    "abrir ópera":          r'"C:\Users\Gc\AppData\Local\Programs\Opera GX\opera.exe"',
    "abrir fifa":           r'"C:\Users\Gc\Desktop\FIFA Mod Manager.url"',
    "abrir spotify":        r'start spotify:playlist:6YWYdE2ZE0Wc5KlgdhvAJe',  # Corregido: comillas de más
    "reiniciar cerebro":    None
}

# —————— 3) Funciones de TTS ——————
def listar_voces():
    """Imprime todas las voces disponibles para diagnóstico."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("\n=== VOCES DISPONIBLES ===")
    for i, v in enumerate(voices):
        print(f"{i}. ID: {v.id}")
        print(f"   Nombre: {v.name}")
        print(f"   Idiomas: {v.languages}")
        print(f"   Género: {v.gender}")
        print("------------------------")
    return voices

def crear_tts():
    engine = pyttsx3.init()
    # Diagnóstico - Comprobar propiedades iniciales
    print(f"Volumen inicial: {engine.getProperty('volume')}")
    print(f"Velocidad inicial: {engine.getProperty('rate')}")
    
    # Listar voces para diagnostico
    voices = engine.getProperty('voices')
    voz_seleccionada = None
    
    # Intento 1: Buscar voces en español
    for v in voices:
        name = v.name.lower()
        vid = v.id.lower()
        if "spanish" in name or "español" in name or "es-" in vid:
            voz_seleccionada = v.id
            print(f"Seleccionada voz española: {v.name}")
            break
    
    # Intento 2: Si no encontró voz española, usar la primera disponible
    if not voz_seleccionada and voices:
        voz_seleccionada = voices[0].id
        print(f"No se encontró voz española, usando: {voices[0].name}")
    
    # Configurar la voz
    if voz_seleccionada:
        try:
            engine.setProperty('voice', voz_seleccionada)
            print(f"Voz configurada: {voz_seleccionada}")
        except Exception as e:
            print(f"Error al configurar voz: {e}")
    
    # Configuración adicional
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 1.0)
    return engine

def hablar(texto: str):
    """Reinicializa el TTS cada vez para garantizar audio."""
    print(f"Cerebro: {texto}")
    try:
        # Usar el driver sapi5 específicamente en Windows
        engine = pyttsx3.init(driverName='sapi5')
        engine.setProperty('rate', 120)
        engine.setProperty('volume', 1.0)
        
        # Intenta usar una voz específica conocida en español
        try:
            engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0')
        except:
            # Si falla, intenta el método normal
            for v in engine.getProperty('voices'):
                if "spanish" in v.name.lower() or "español" in v.name.lower():
                    engine.setProperty('voice', v.id)
                    break
        
        print("Intentando reproducir audio...")
        engine.say(texto)
        engine.runAndWait()
        print("Audio reproducido correctamente")
    except Exception as e:
        print(f"ERROR DE VOZ: {e}")
        # Intento alternativo con configuración mínima
        try:
            print("Intento alternativo de voz...")
            simple_engine = pyttsx3.init()
            simple_engine.say(texto)
            simple_engine.runAndWait()
        except Exception as e2:
            print(f"ERROR FATAL DE VOZ: {e2}")

# Ejecutar diagnóstico de voces al inicio
print("=== DIAGNÓSTICO DE SISTEMA DE VOZ ===")
voces_disponibles = listar_voces()
print(f"Total de voces disponibles: {len(voces_disponibles)}")

# Precalentar TTS para evitar latencia
try:
    _tt = crear_tts()
    _tt.say("Sistema activado")
    _tt.runAndWait()
    print("Precalentamiento de voz exitoso")
except Exception as e:
    print(f"Error en precalentamiento de voz: {e}")

# —————— 4) Precalentar audio micro ——————
_SR = 16000
try:
    sd.rec(int(0.1 * _SR), samplerate=_SR, channels=1)
    sd.wait()
except:
    pass

# —————— 5) Grabación y reconocimiento ——————
def grabar(segundos=3):
    return sd.rec(int(segundos * _SR), samplerate=_SR, channels=1, dtype='int16')

def reconocer(audio_bytes):
    audio = sr.AudioData(audio_bytes, _SR, 2)
    recog = sr.Recognizer()
    try:
        return recog.recognize_google(audio, language="es-ES").lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        hablar("Error de servicio.")
        return None

# —————— 6) Modo Comando (F9) ——————
def modo_comando():
    hablar("Di tu comando.")
    rec = grabar(3)
    sd.wait()
    cmd = reconocer(rec.tobytes())
    if not cmd:
        hablar("No te entendí.")
        return

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

# —————— 7) Modo IA (F10) ——————
def modo_ia():
    try:
        hablar("¿Qué quieres preguntarle a la IA?")
        rec = grabar(5)
        sd.wait()
        pregunta = reconocer(rec.tobytes())
        if not pregunta:
            hablar("No entendí tu pregunta.")
            return

        hablar("Pensando…")
        # —> PROMPT EN ESPAÑOL
        prompt = (
            "Eres un asistente experto que siempre RESPONDE en español.\n"
            f"Usuario: {pregunta}\n"
            "IA:"
        )
        print(f"Enviando pregunta a LLM: {pregunta}")
        resp = llm(prompt, max_tokens=128)
        texto = resp['choices'][0]['text'].strip()
        print(f"Respuesta recibida: {texto}")
        if texto:
            print("Intentando reproducir respuesta por voz...")
            hablar(texto)
        else:
            hablar("La IA no devolvió respuesta.")
    except Exception as e:
        print(f"ERROR EN MODO IA: {e}")
        hablar("Ocurrió un error al procesar tu pregunta.")

# —————— 8) Bucle de teclas ——————
hablar("Listo. Pulsa F9 para comandos o F10 para IA.")
print("CONTROLES: F9=Comandos, F10=IA, F8=Prueba de voz")
while True:
    evento = keyboard.read_event()
    if evento.event_type == keyboard.KEY_DOWN:
        if evento.name == "f9":
            modo_comando()
        elif evento.name == "f10":
            modo_ia()
        elif evento.name == "f8":
            # Prueba de voz con diferentes métodos
            print("\n=== PRUEBA DE VOZ ===")
            try:
                print("1. Método estándar")
                hablar("Esto es una prueba de voz con el método principal.")
                
                print("\n2. Método alternativo con SAPI5 directo")
                engine_alt = pyttsx3.init(driverName='sapi5')
                engine_alt.setProperty('rate', 120)
                engine_alt.setProperty('volume', 1.0)
                engine_alt.say("Prueba alternativa con SAPI5.")
                engine_alt.runAndWait()
                
                print("\n3. Método con propiedades por defecto")
                engine_def = pyttsx3.init()
                engine_def.say("Prueba con propiedades por defecto.")
                engine_def.runAndWait()
                
                print("Pruebas de voz completadas")
            except Exception as e:
                print(f"Error durante pruebas de voz: {e}")
