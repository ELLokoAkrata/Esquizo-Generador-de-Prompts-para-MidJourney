# Documentación del Agente: Esquizo-Generador de Prompts

## 1. Resumen del Sistema

Este proyecto es una aplicación Streamlit que implementa un flujo de trabajo de dos fases para generar prompts de alta calidad para modelos de texto a imagen como MidJourney. El sistema aprovecha un modelo de IA especializado para el análisis visual y permite al usuario elegir entre varios modelos de lenguaje para la síntesis creativa.

El objetivo es permitir al usuario refinar sus ideas creativas, utilizando opcionalmente una imagen de referencia, y traducir la intención del usuario en prompts ricos y evocadores, con la flexibilidad de experimentar diferentes "estilos" de IA.

## 2. Arquitectura y Flujo de Datos

El sistema opera en un pipeline secuencial que se activa al presionar el botón "Generar Prompts".

**Componentes Principales:**

*   **Frontend:** Interfaz de usuario construida con Streamlit (`prompt_generator_st.py`).
*   **Lógica de Orquestación:** Contenida en el mismo script, maneja el estado de la sesión (ej. modelo seleccionado) y las llamadas a la API de Groq.
*   **Modelo de Visión (Fase 1):** `meta-llama/llama-4-scout-17b-16e-instruct` (rol fijo).
*   **Modelos de Lenguaje (Fase 2):** Seleccionable por el usuario. Las opciones son:
    *   `openai/gpt-oss-20b`
    *   `deepseek-r1-distill-llama-70b`
    *   `moonshotai/kimi-k2-instruct`

**Flujo de Datos:**

1.  **Entrada del Usuario:**
    *   `uploaded_file` (Opcional): Una imagen (JPG, PNG).
    *   `user_idea` (Requerido): Un texto que describe la transformación deseada.
    *   `selected_model`: El modelo de lenguaje elegido en la barra lateral.
    *   `num_variations`: El número de prompts a generar.

2.  **Fase 1: Análisis de Visión (Si se proporciona una imagen)**
    *   La imagen se codifica en base64 y se envía al modelo `meta-llama/llama-4-scout-17b-16e-instruct`.
    *   **Prompt del Sistema (Visión):** "You are an expert image analyst..."
    *   **Salida:** Una descripción textual detallada de la imagen (`image_description`).

3.  **Fase 2: Síntesis Creativa**
    *   Se construye un `final_user_prompt` combinando la `image_description` (si existe) con la `user_idea`.
    *   Se inicia un bucle para `num_variations`. En cada iteración:
        *   Se realiza una llamada a la API de Groq utilizando el `selected_model`.
        *   **Lógica de Variaciones:** La conversación con la IA se mantiene en el estado de la sesión. Para cada nueva variación, se añaden las respuestas anteriores al historial de mensajes y se le pide explícitamente a la IA que genere algo "completamente diferente". Esto asegura la diversidad de los resultados.
    *   **Prompt del Sistema (Texto):** "Eres un generador de prompts para MidJourney..."
    *   **Salida:** Un prompt creativo para MidJourney.

4.  **Salida a la Interfaz:** Los prompts generados se muestran en la interfaz de Streamlit.

## 3. Modelos Utilizados

### Modelo de Visión (El Ojo)

*   **`meta-llama/llama-4-scout-17b-16e-instruct`**
    *   **Rol:** Analista Visual.
    *   **Fortalezas:** Multimodalidad nativa, ideal para extraer detalles, atmósfera y composición de una imagen.
    *   **Uso:** Proporciona una descripción objetiva y detallada que sirve como base para la fase creativa.

### Modelos de Lenguaje (Las Voces)

El usuario puede seleccionar uno de los siguientes modelos para la tarea de síntesis creativa. Cada uno ofrece un "sabor" distinto.

*   **`openai/gpt-oss-20b` (La Voz Original)**
    *   **Rol:** Sintetizador Creativo Equilibrado.
    *   **Fortalezas:** Buen razonamiento y seguimiento de instrucciones complejas. Un modelo versátil para la generación de texto poético.

*   **`deepseek-r1-distill-llama-70b` (El Destilador)**
    *   **Rol:** Generador Enfocado y Estructurado.
    *   **Fortalezas:** Como modelo "destilado", puede producir resultados más concisos o centrados en la directiva principal del usuario.

*   **`moonshotai/kimi-k2-instruct` (El Poeta Abstracto)**
    *   **Rol:** Generador Narrativo y Expansivo.
    *   **Fortalezas:** Conocido por su gran ventana de contexto y fuertes habilidades de lenguaje, puede ser ideal para crear prompts más abstractos, narrativos o con detalles intrincados.

## 4. Dependencias Clave

*   `streamlit`: Para la interfaz de usuario.
*   `groq`: Para la interacción con los modelos de IA.

El archivo `requirements.txt` contiene la lista completa.