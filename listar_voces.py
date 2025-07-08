import sounddevice as sd

# Lista todos los dispositivos de audio
for idx, dev in enumerate(sd.query_devices()):
    print(f"{idx}: {dev['name']} — {dev['max_input_channels']} canales de entrada")
