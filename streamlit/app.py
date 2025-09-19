#----------------------------
# Fecha de creación: 20250911 
# Fecha de modificación: 20250913
# Autores: 
# - Jorge Hierro Francoy 
# - Javier Miranda Pascual
#----------------------------

# LIBRERÍAS

import streamlit as st
from openai import OpenAI
import base64
import requests

from pedIAclick import buscar_info_brave, generar_post, generar_prompt_imagen, generar_prompt_imagen, generar_imagen_dalle

# CONFIG
BRAVE_TOKEN = st.secrets.get("BRAVE_TOKEN", "")
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
OPENAI_KEY_IMAGES = st.secrets.get("OPENAI_API_KEY_IMAGES", "")

client = OpenAI(api_key=OPENAI_KEY)
client_images = OpenAI(api_key=OPENAI_KEY_IMAGES)

#######################################################################################################################

st.title("👶 pedIAclick")
st.write("Generador de posts e imágenes para redes sociales basado en la AEP.")


tema_post = st.text_input("Introduce el tema del post (ej. 'Consumo de fruta en bebés')")

# Variable de sesión para guardar el post
if "post_generado" not in st.session_state:
    st.session_state.post_generado = None

if st.button("Generar post"):
    if not tema_post:
        st.warning("Por favor, escribe un tema antes de generar el post.")
    else:
        with st.spinner("🔎 Buscando información en la AEP..."):
            llm_text = buscar_info_brave(tema_post, BRAVE_TOKEN)
        
        with st.spinner("✍️ Creando post con GPT..."):
            try:
                post = generar_post(tema_post, llm_text, client)
                st.session_state.post_generado = post
            except Exception as e:
                st.error(f"⚠️ Error al generar el post con GPT: {e}")
                st.session_state.post_generado = None
        
        if st.session_state.post_generado:
            st.subheader("📌 Post generado:")
            st.write(st.session_state.post_generado)

if st.session_state.post_generado:
    if st.button("🎨 Generar imagen del post"):
        with st.spinner("🖼️ Creando prompt para imagen..."):
            try:
                ruta_imagen = "assets/referencia.jpeg"
                prompt_img = generar_prompt_imagen(st.session_state.post_generado, ruta_imagen)

                with st.spinner("🎨 Generando imagen con DALL·E..."):
                    image_result = generar_imagen_dalle(prompt_img)
                
                    if image_result:
                        st.image(image_result, caption="🖼️ Imagen generada por DALL·E")
                        st.success("✅ Imagen generada con éxito")
                    else:
                        st.error("⚠️ No se pudo generar la imagen. Verifica tu API Key y límites de facturación.")

                with st.expander("📖 Ver texto completo del post"):
                    st.write(st.session_state.post_generado)

            except Exception as e:
                st.error(f"⚠️ Error al generar el prompt de imagen: {e}")
