import os
import subprocess
import sys
import time  # Importar time para usar sleep

def main():
    try:
        # Activar el entorno virtual
        print("Activando el entorno virtual...")
        # Detectar sistema operativo y usar el comando adecuado
        if os.name == "nt":
            activate_command = "venv\\Scripts\\activate.bat"
        else:
            activate_command = "source venv/Scripts/activate"
        subprocess.run(activate_command, shell=True, check=True)

        # Esperar 2 segundos para asegurar que el entorno virtual se inicie correctamente
        time.sleep(2)

        # Ejecutar cerebro.py
        print("Iniciando Cerebro...")
        subprocess.run([sys.executable, "cerebro.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
