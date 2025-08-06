# Esquizo-Generador de Prompts para MidJourney

Una herramienta de Streamlit para la generación de prompts de alta calidad para MidJourney, utilizando un flujo de trabajo de dos etapas que combina el análisis de imágenes con la generación de texto creativo.

## Flujo de Trabajo

1.  **Análisis Visual (Opcional):** Carga una imagen. Un modelo de IA de visión (`llama-4-scout`) la analizará y generará una descripción detallada de sus elementos, atmósfera y estilo.
2.  **Síntesis Creativa:** Escribe una idea o directiva. Otro modelo de IA de lenguaje (`openai/gpt-oss-20b`) fusionará la descripción de la imagen (si se proporciona) con tu idea para crear prompts evocadores y poéticos.

## Uso

1.  Clona el repositorio.
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Asegúrate de tener tu clave de API de Groq configurada como una variable de entorno (`GROQ_API_KEY`).
4.  Ejecuta la aplicación:
    ```bash
    streamlit run prompt_generator_st.py
    ```
