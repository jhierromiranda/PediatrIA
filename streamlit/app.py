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

from pedIAclick import buscar_info_brave, generar_post

# CONFIG
BRAVE_TOKEN = st.secrets.get("BRAVE_TOKEN", "")
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")

# Inicializamos cliente GPT
client = OpenAI(api_key=OPENAI_KEY)


#########################################################################################################################

# INTERFAZ STREAMLIT

st.set_page_config(page_title="pedIAtria", page_icon="👶", layout="centered")

st.title("👶 pedIAtria")
st.write("Generador de posts para redes sociales basado en información de la Asociación Española de Pediatría (AEP).")

tema_post = st.text_input("Introduce el tema del post (ej. 'Consumo de fruta en bebés')")

if st.button("Generar post"):
    if not tema_post:
        st.warning("Por favor, escribe un tema antes de generar el post.")
    else:
        with st.spinner("🔎 Buscando información en la AEP..."):
            llm_text = buscar_info_brave(tema_post, BRAVE_TOKEN)
        
        with st.spinner("✍️ Creando post con GPT..."):
            try:
                post = generar_post(tema_post, llm_text, client)
            except Exception as e:
                st.error(f"⚠️ Error al generar el post con GPT: {e}")
                post = None
        
        if post:
            st.subheader("📌 Post generado:")
            st.write(post)