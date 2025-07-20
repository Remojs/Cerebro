# Cerebro: Asistente por Voz con Integración de IA

Cerebro es un asistente por voz en desarrollo que combina comandos de voz básicos con una integración de inteligencia artificial (IA) para responder preguntas y realizar tareas automatizadas. Este proyecto está diseñado para ser una herramienta versátil y personalizable, ideal para mejorar la productividad y la experiencia del usuario.

## Características Principales

- **Comandos por Voz**: Ejecuta aplicaciones y tareas predefinidas mediante comandos de voz.
- **Integración de IA**: Responde preguntas utilizando un modelo de lenguaje basado en Llama v2.
- **Modos Preconfigurados**: Permite lanzar múltiples aplicaciones relacionadas con un contexto específico (como "juego", "programación" o "estudio").
- **Interfaz Simple**: Controlado mediante teclas rápidas y comandos de voz.
- **Rutas Centralizadas**: Todas las rutas de aplicaciones están definidas en un archivo separado (`utils/paths.py`) para facilitar la personalización.

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
- `abrir photoshop`: Abre Adobe Photoshop.
- `abrir steam`: Abre la plataforma de juegos Steam.
- `abrir gpt`: Abre ChatGPT en el navegador predeterminado.
- `reiniciar cerebro`: Reinicia el asistente.

### Modos Preconfigurados (F8)
- **modo juego**: Lanza Steam y Discord.
- **modo programación**: Abre Visual Studio Code, Opera GX y Obsidian.
- **modo estudio**: Abre Google Chrome (perfil de estudio) y Mendeley.

## Cómo Funciona

1. **Modo Comando (F9)**:
   - Emite un beep para indicar que está escuchando.
   - Escucha un comando de voz durante 2 segundos.
   - Reconoce el comando y ejecuta la acción correspondiente.
   - Si no reconoce el comando, informa al usuario.

2. **Modo IA (F10)**:
   - Escucha una pregunta del usuario durante 2.5 segundos.
   - Procesa la pregunta utilizando un modelo de lenguaje (Llama v2).
   - Responde en español tanto por texto como por voz.

3. **Modo por Voz (F8)**:
   - Escucha el nombre de un modo preconfigurado (como "modo juego" o "modo programación").
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
  - `winsound` (solo Windows)

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
   venv\Scripts\activate
   ```
4. Ejecuta el script principal:
   ```bash
   python cerebro.py
   ```

## Arquitectura Técnica

Cerebro está diseñado con una arquitectura modular que facilita su mantenimiento y expansión:

- **Módulo de Reconocimiento de Voz**: Utiliza `speech_recognition` y `sounddevice` para capturar y procesar comandos de voz.
- **Módulo de Síntesis de Voz**: Implementa `pyttsx3` para la conversión de texto a voz con soporte para voces en español.
- **Módulo de IA**: Integra el modelo Llama v2 para responder preguntas utilizando procesamiento de lenguaje natural.
- **Gestor de Comandos**: Maneja la ejecución de aplicaciones y tareas basadas en comandos de voz.
- **Gestor de Modos**: Administra conjuntos preconfigurados de aplicaciones para diferentes contextos de trabajo.

## Próximas Características

### 1. Integración de Calendario IA

**Descripción**: Gestión completa del Google Calendar mediante comandos de voz naturales.

**Implementación Técnica**:
- Microservicio REST en FastAPI con autenticación OAuth2 para Google Calendar API
- Endpoints para crear, editar, borrar y consultar eventos
- Integración con el módulo de IA mediante Function Calling
- Parseador de lenguaje natural para extraer fechas, horas y duración de eventos

**Funcionalidades**:
- Crear eventos: "Agenda una reunión con Juan mañana a las 3 PM"
- Consultar agenda: "¿Qué tengo hoy?" o "Muéstrame mis pendientes para la semana"
- Modificar eventos: "Cambia mi cita del jueves para el viernes"
- Sincronización bidireccional con interfaz visual

### 2. Gestión de Memorias en Obsidian

**Descripción**: Sistema para almacenar y recuperar información estructurada en Obsidian como base de conocimiento.

**Implementación Técnica**:
- Integración con la API de Obsidian mediante `python-frontmatter`
- Sistema de observación de cambios con `watchdog`
- Estructura de archivos Markdown para tareas, proyectos y contexto
- Sincronización bidireccional con Google Calendar

**Funcionalidades**:
- Guardar información: "Guarda que necesito comprar leche"
- Consultar notas: "¿Qué tengo pendiente del proyecto Cerebro?"
- Organización automática por tags y categorías
- Mantenimiento de coherencia entre fuentes de datos

### 3. Consultas en Tiempo Real

**Descripción**: Capacidad para obtener información actualizada de fuentes externas bajo demanda.

**Implementación Técnica**:
- Integración con APIs externas (OpenWeatherMap, CoinGecko, NewsAPI)
- Framework de herramientas (Tools) para Function Calling
- Cache inteligente para optimizar consultas frecuentes
- Sistema de formateo para resultados coherentes

**Funcionalidades**:
- Consultas meteorológicas: "¿Cómo estará el clima mañana en Madrid?"
- Información financiera: "¿Cuál es el precio actual de Bitcoin?"
- Noticias: "Dime las últimas noticias de tecnología"
- Traductor: "Traduce 'Buenos días' al inglés"

### 4. Mini-Interfaz de Escritorio

**Descripción**: Interfaz gráfica minimalista para visualizar y controlar el asistente.

**Implementación Técnica**:
- Desarrollo con Tauri (Rust + WebView) para mayor eficiencia
- Comunicación mediante WebSockets con el backend de Python
- Diseño responsive y minimalista con React
- Sistema de notificaciones y visualización de estados

**Funcionalidades**:
- Visualización del historial de comandos y respuestas
- Control manual de funciones del asistente
- Panel de configuración para personalizar comportamientos
- Indicadores visuales de estado (escuchando, procesando, respondiendo)

### 5. Auto-arranque y Despliegue

**Descripción**: Sistema para mantener el asistente activo desde el inicio del sistema.

**Implementación Técnica**:
- Empaquetado con PyInstaller para crear ejecutable independiente
- Configuración de inicio automático mediante registro de Windows
- Versiones alternativas para Linux (systemd) y macOS (launchd)
- Sistema de actualizaciones automáticas

**Funcionalidades**:
- Inicio automático con el sistema
- Operación en segundo plano con mínimo uso de recursos
- Recuperación ante errores y reinicio automático
- Configuración de nivel de permisos y acceso

## Estado del Proyecto

Cerebro está en desarrollo activo. La versión actual incluye las funcionalidades básicas de reconocimiento de voz, ejecución de comandos y respuestas mediante IA. Las próximas características se implementarán según la hoja de ruta establecida.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas, sugerencias o encuentras errores, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
