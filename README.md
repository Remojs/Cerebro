# Cerebro: Asistente por Voz con Integración de IA

Cerebro es un asistente por voz en desarrollo que combina comandos de voz básicos con una integración de inteligencia artificial (IA) para responder preguntas y realizar tareas automatizadas. Este proyecto está diseñado para ser una herramienta versátil y personalizable, ideal para mejorar la productividad y la experiencia del usuario.

## Características Principales

- **Comandos por Voz**: Ejecuta aplicaciones y tareas predefinidas mediante comandos de voz.
- **Integración de IA**: Responde preguntas utilizando un modelo de lenguaje basado en Llama v2.
- **Modos Preconfigurados**: Permite lanzar múltiples aplicaciones relacionadas con un contexto específico (como "juego", "programación" o "estudio").
- **Interfaz Simple**: Controlado mediante teclas rápidas y comandos de voz.
- **Rutas Centralizadas**: Todas las rutas de aplicaciones están definidas en un archivo separado (`paths.py`) para facilitar la personalización.

## Comandos Básicos

### Teclas Rápidas
- **F9**: Activa el modo de comandos por voz. Permite ejecutar aplicaciones o tareas predefinidas.
- **F10**: Activa el modo de IA. Responde preguntas utilizando el modelo de lenguaje.
- **F8**: Activa el modo por voz para seleccionar un conjunto de aplicaciones preconfiguradas (modos).

### Comandos Disponibles (F9)
- `abrir visual studio`: Abre Visual Studio Code.
- `abrir notas`: Abre Obsidian.
- `abrir ópera`: Abre el navegador Opera GX.
- `abrir fifa`: Abre el gestor de FIFA Mod Manager.
- `abrir spotify`: Abre una lista de reproducción específica en Spotify.
- `reiniciar cerebro`: Reinicia el asistente.

### Modos Preconfigurados (F8)
- **juego**: Lanza Steam y Discord.
- **programación**: Abre Visual Studio Code, Opera GX y Obsidian.
- **estudio**: Abre Google Chrome (perfil de estudio) y Mendeley.

## Cómo Funciona

1. **Modo Comando (F9)**:
   - Escucha un comando de voz durante 2.5 segundos.
   - Reconoce el comando y ejecuta la acción correspondiente.
   - Si no reconoce el comando, informa al usuario.

2. **Modo IA (F10)**:
   - Escucha una pregunta del usuario durante 2 segundos.
   - Procesa la pregunta utilizando un modelo de lenguaje (Llama v2).
   - Responde en español tanto por texto como por voz.

3. **Modo por Voz (F8)**:
   - Escucha el nombre de un modo preconfigurado (como "juego" o "programación").
   - Lanza las aplicaciones asociadas al modo seleccionado.

## Requisitos

- **Python 3.8+**
- Bibliotecas necesarias:
  - `sounddevice`
  - `speech_recognition`
  - `pyttsx3`
  - `keyboard`
  - `subprocess`
  - `llama_cpp`

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Remojs/Cerebro.git
   ```
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
3. Activa el entorno virtual:
   ```bash
   source venv/Scripts/activate
   ```
4. Ejecuta el script principal:
   ```bash
   python cerebro.py
   ```

## Estado del Proyecto

Cerebro está en desarrollo activo. Algunas características pueden no estar completamente implementadas o ser inestables. Se planea agregar más comandos, mejorar la integración de IA y optimizar la experiencia del usuario.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas, sugerencias o encuentras errores, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
