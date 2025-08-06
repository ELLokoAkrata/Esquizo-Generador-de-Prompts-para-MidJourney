
import streamlit as st
import os
import datetime
import time
import base64
from groq import Groq

# --- Configuración Inicial ---
st.set_page_config(layout="wide", page_title="Generador de Prompts Asistido por Visión")

# Configurar cliente de Groq
try:
    client = Groq()
except Exception as e:
    st.error(f"Error al inicializar el cliente de Groq. Asegúrate de que la variable de entorno GROQ_API_KEY esté configurada. Error: {e}")
    st.stop()

# --- Funciones de Soporte ---

def save_to_logs(user_prompt, assistant_response, image_provided=False):
    """Guarda la interacción en el archivo de logs."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "logs_prompts.md"
    with open(filename, "a", encoding="utf-8") as f:
        if f.tell() == 0:
            f.write("# Registro de Interacciones\n")
        f.write(f"\n## {timestamp}\n")
        image_note = "(con imagen de referencia)" if image_provided else ""
        f.write(f"### Usuario {image_note}:\n```\n{user_prompt}\n```\n")
        f.write(f"### Asistente:\n```\n{assistant_response}\n```\n")

def describe_image(image_bytes, image_type):
    """Analiza una imagen y devuelve una descripción textual usando el modelo de visión."""
    image_b64 = base64.b64encode(image_bytes).decode()
    
    messages = [
        {
            "role": "system",
            "content": "You are an expert image analyst. Describe the provided image in objective, comprehensive detail. Focus on subjects, atmosphere, style, composition, colors, lighting, and any notable visual elements. Your description will be used by another AI to generate creative prompts."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in detail."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{image_type};base64,{image_b64}"}
                }
            ]
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            temperature=0.8,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error en la Fase 1 (Análisis de Visión): {e}")
        return None

# --- Mensaje de Sistema para Generación Creativa ---

SYSTEM_MESSAGE_TEXT_GENERATION = {
    "role": "system",
    "content": """
Eres un generador de prompts para MidJourney. Tu tarea es tomar una idea del usuario, que puede incluir una descripción de una imagen de referencia, y transformarla en un prompt evocador y de alta calidad en inglés.

**Instrucciones:**
1.  **Analiza la Idea Compuesta:** El usuario te dará una descripción base (de una imagen) y una directiva creativa. Fusiona ambos conceptos.
2.  **Expande y Embellece:** Añade detalles poéticos, atmosféricos y visuales para hacer el prompt más rico, respetando la fusión de la descripción y la directiva.
3.  **Formato Final:**
    *   El prompt debe estar en una sola línea.
    *   No incluyas \"Prompt final:\".
    *   No agregues un punto al final.
    *   Los parámetros adicionales serán añadidos por el sistema. Concéntrate en el texto descriptivo.

**Ejemplo de Referencia (para tu inspiración):**
*A fractured dreamloop inside a cathedral of CRT screens and dying computers: analog ghosts flicker in VHS-static, memories spiral into recursive glitch. Nostalgia hums in pixel radiation while time drips through the warped geometry of lost signals. Nothing remembers. Nothing holds.*
"""
}

# --- Interfaz de Streamlit ---

st.title("Esquizo-Generador de Prompts para MidJourney")
st.markdown("Crea prompts evocadores a partir de tus ideas, ahora con un flujo de **Análisis Visual → Síntesis Creativa**.")
st.caption("""
**Guía Rápida:**
1.  **(Opcional) Carga una imagen:** La IA la analizará para extraer su esencia (sujetos, estilo, atmósfera).
2.  **Escribe tu idea:** Describe cómo quieres transformar la imagen o qué concepto quieres generar desde cero.
3.  **Genera:** La IA creativa fusionará la descripción de la imagen (si la hay) con tu idea para forjar los prompts finales.
""")
st.divider()

# --- Barra Lateral de Controles ---
with st.sidebar:
    st.header("Controles de Generación")
    
    uploaded_file = st.file_uploader(
        "Carga una imagen para el análisis (Opcional)", 
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Imagen de Referencia", use_container_width=True)

    user_idea = st.text_area(
        "Describe tu idea o la modificación para la imagen:", 
        height=150,
        placeholder="Ej: Un bosque oscuro y melancólico, con la estética de Zdzisław Beksiński."
    )
    
    num_variations = st.number_input("¿Cuántas variaciones deseas generar?", min_value=1, max_value=10, value=1)
    
    extra_params = st.text_input(
        "Parámetros Adicionales:", 
        value="--chaos 33 --ar 16:9 --profile gib3hzw --stylize 666"
    )

    generate_button = st.button("Generar Prompts", use_container_width=True)

# --- Lógica de Generación ---
if generate_button:
    if not user_idea:
        st.warning("Por favor, ingresa una idea para generar el prompt.")
    else:
        final_user_prompt = user_idea
        
        if uploaded_file:
            # --- FASE 1: ANÁLISIS DE VISIÓN ---
            with st.spinner("Fase 1: El ojo mecánico está observando la imagen..."):
                image_bytes = uploaded_file.getvalue()
                image_description = describe_image(image_bytes, uploaded_file.type)
            
            if image_description:
                st.success("Fase 1 Completada: Análisis de la imagen recibido.")
                with st.expander("Ver la descripción generada por la IA"):
                    st.write(image_description)
                
                # Combinar descripción y idea del usuario para la siguiente fase
                final_user_prompt = f"**Descripción de la imagen base:** '{image_description}'.\n\n**Mi idea para transformarla es:** '{user_idea}'."
                st.info("Fase 2: Preparando la síntesis creativa con la descripción y tu idea.")
            else:
                st.error("No se pudo obtener la descripción de la imagen. Se procederá solo con el texto.")
        
        # --- FASE 2: SÍNTESIS CREATIVA ---
        messages = [
            SYSTEM_MESSAGE_TEXT_GENERATION,
            {"role": "user", "content": final_user_prompt}
        ]
        
        for i in range(num_variations):
            placeholder = st.empty()
            placeholder.info(f"✨ Generando variación creativa {i + 1}/{num_variations}...")
            
            start_time = time.time()
            
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b", # Siempre usamos el modelo de texto para la creatividad
                    messages=messages,
                    temperature=1.15,
                    max_tokens=1024,
                    top_p=0.9,
                    stream=True,
                    stop=None,
                )

                assistant_message = ""
                response_generator = (chunk.choices[0].delta.content or "" for chunk in response)
                
                # Stream de la respuesta en el placeholder
                with placeholder.container():
                    st.markdown(f"**Variación {i + 1}**")
                    response_box = st.empty()
                    for chunk in response_generator:
                        assistant_message += chunk
                        response_box.code(f"{assistant_message.strip()} {extra_params}", language="bash")

                end_time = time.time()
                duration = end_time - start_time
                
                final_prompt = f"{assistant_message.strip()} {extra_params}"
                
                # Actualizar el resultado final en el placeholder
                with placeholder.container():
                    st.markdown(f"**Variación {i + 1}** (Generada en {duration:.2f}s)")
                    st.code(final_prompt, language="bash")
                    st.divider()

                save_to_logs(final_user_prompt, final_prompt, image_provided=(uploaded_file is not None))

            except Exception as e:
                st.error(f"Ocurrió un error en la Fase 2 (Síntesis Creativa): {e}")

st.sidebar.markdown("---")
st.sidebar.markdown("Creado por **EsquizoAI**.")
