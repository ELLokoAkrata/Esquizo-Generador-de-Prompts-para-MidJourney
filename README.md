# Esquizo-Generador de Prompts para MidJourney

Una herramienta de Streamlit para la generación de prompts de alta calidad para MidJourney, utilizando un flujo de trabajo de dos etapas que combina el análisis de imágenes con la generación de texto creativo.

## Flujo de Trabajo

1.  **Análisis Visual (Opcional):** Carga una imagen. Un modelo de IA de visión (`llama-4-scout`) la analizará y generará una descripción detallada de sus elementos, atmósfera y estilo.
2.  **Síntesis Creativa:** Escribe una idea o directiva. Un modelo de IA de lenguaje fusionará la descripción de la imagen (si se proporciona) con tu idea para crear prompts evocadores y poéticos.

## Nuevas Características (Agosto 2025)

-   **Generación de Variaciones Corregida:** Se ha solucionado un error que causaba que se generaran prompts idénticos al solicitar múltiples variaciones. Ahora, la IA mantiene el contexto de las generaciones anteriores para producir resultados únicos y diversos en cada iteración.
-   **Selector de Modelos de IA:** Se ha añadido un selector en la barra lateral que permite elegir entre diferentes modelos de lenguaje para la fase de síntesis creativa. Esto permite experimentar con distintos "sabores" de IA. Los modelos disponibles son:
    -   `openai/gpt-oss-20b` (Original)
    -   `deepseek-r1-distill-llama-70b`
    -   `moonshotai/kimi-k2-instruct`
-   **Estabilidad Mejorada:** Se corrigió un error que provocaba que la aplicación se quedara en estado de "ejecución" al cambiar de modelo.

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