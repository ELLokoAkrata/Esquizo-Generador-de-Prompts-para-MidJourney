# AGENT_DOCUMENTATION.md

## Esquizo-Generador de Prompts para MidJourney

### 1. Resumen del Sistema

Este proyecto es una aplicación Streamlit que implementa un flujo de trabajo de dos fases para generar prompts de alta calidad para modelos de texto a imagen como MidJourney. El sistema aprovecha las capacidades especializadas de dos modelos de IA distintos: uno para el análisis visual y otro para la síntesis creativa de texto.

El objetivo es permitir al usuario refinar sus ideas creativas utilizando una imagen de referencia como punto de partida, traduciendo la esencia visual de la imagen y la intención del usuario en un prompt rico y evocador.

### 2. Arquitectura y Flujo de Datos

El sistema opera en un pipeline secuencial que se activa al presionar el botón "Generar Prompts".

**Componentes Principales:**

*   **Frontend:** Interfaz de usuario construida con Streamlit (`prompt_generator_st.py`).
*   **Backend Logic:** Contenida en el mismo script de Streamlit, orquesta las llamadas a la API de Groq.
*   **Modelo de Visión (Fase 1):** `meta-llama/llama-4-scout-17b-16e-instruct`
*   **Modelo de Lenguaje (Fase 2):** `openai/gpt-oss-20b`

**Flujo de Datos:**

1.  **Entrada del Usuario:**
    *   `uploaded_file` (Opcional): Una imagen (JPG, PNG) cargada por el usuario.
    *   `user_idea` (Requerido): Un texto que describe la transformación deseada o la idea creativa.

2.  **Fase 1: Análisis de Visión (Si se proporciona una imagen)**
    *   La imagen se codifica en base64.
    *   Se realiza una llamada a la API de Groq utilizando el modelo `meta-llama/llama-4-scout-17b-16e-instruct`.
    *   **Prompt del Sistema (Visión):** "You are an expert image analyst. Describe the provided image in objective, comprehensive detail..."
    *   **Salida:** Una descripción textual detallada de la imagen (`image_description`).

3.  **Fase 2: Síntesis Creativa**
    *   Se construye un `final_user_prompt`.
        *   **Si hubo imagen:** Se combina la `image_description` con la `user_idea` en un formato estructurado: "**Descripción de la imagen base:** '{image_description}'.\n\n**Mi idea para transformarla es:** '{user_idea}'."
        *   **Si no hubo imagen:** Se utiliza directamente la `user_idea`.
    *   Se realiza una llamada a la API de Groq utilizando el modelo `openai/gpt-oss-20b`.
    *   **Prompt del Sistema (Texto):** "Eres un generador de prompts para MidJourney. Tu tarea es tomar una idea del usuario..."
    *   **Salida:** El prompt final para MidJourney, generado de forma creativa.

4.  **Salida a la Interfaz:** El prompt generado se muestra en la interfaz de Streamlit.

### 3. Modelos Utilizados

*   **`meta-llama/llama-4-scout-17b-16e-instruct`**
    *   **Rol:** Analista Visual (El Ojo).
    *   **Fortalezas:** Multimodalidad nativa, gran ventana de contexto, arquitectura de Mezcla de Expertos (MoE). Ideal para extraer detalles, atmósfera y composición de una imagen.
    *   **Uso:** Se le pide que actúe como un experto analista de imágenes para proporcionar una descripción objetiva y detallada.

*   **`openai/gpt-oss-20b`**
    *   **Rol:** Sintetizador Creativo (La Voz).
    *   **Fortalezas:** Razonamiento avanzado, seguimiento de instrucciones complejas, arquitectura MoE eficiente para tareas de lenguaje.
    *   **Uso:** Se le pide que actúe como un generador de prompts, fusionando la descripción visual (si existe) con la directiva del usuario para crear un texto poético y evocador.

### 4. Dependencias Clave

*   `streamlit`: Para la interfaz de usuario.
*   `groq`: Para la interacción con los modelos de IA.

El archivo `requirements.txt` contiene la lista completa de dependencias.

### 5. Puntos de Extensión Futura

*   **Animación de Prompts:** Utilizar la descripción de la imagen y el prompt generado para crear animaciones cortas (image-to-video).
*   **Selección de Estilo:** Permitir al usuario seleccionar estilos artísticos predefinidos (ej. Cyberpunk, Ghibli, Beksiński) que se añaden al contexto de la Fase 2.
*   **Carga de Múltiples Imágenes:** Permitir el análisis de varias imágenes para fusionar conceptos.
