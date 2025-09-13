#########################################################################################################################
##################################################### pedIAclick ########################################################
#########################################################################################################################
import requests
import streamlit as st
from openai import OpenAI


#########################################################################################################################
# CONFIG
#########################################################################################################################
BRAVE_TOKEN = st.secrets.get("BRAVE_TOKEN", "")
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_KEY)


#########################################################################################################################
# FUNCIONES AUXILIARES
#########################################################################################################################

def buscar_info_brave(tema_post: str) -> str:
    url = 'https://api.search.brave.com/res/v1/web/search'
    query = f'site:aeped.es {tema_post}'
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "x-subscription-token": BRAVE_TOKEN
    }
    params = {'q': query, "extra_snippets": "true"}
    
    try:
        response = requests.get(url, headers=headers, params=params).json()
    except Exception as e:
        return f"⚠️ Error al conectar con Brave API: {e}"
    
    llm_text = ""
    if 'results' in response.get('web', {}) and len(response['web']['results']) > 0:
        llm_text += f'{query}. '
        for j, res in enumerate(response['web']['results']):
            if 'extra_snippets' in res:
                llm_text += f"Descripcion {j+1}: {res['title']} {res['extra_snippets']}. "
            else:
                llm_text += f"Descripcion {j+1}: {res['title']}. "
    else:
        llm_text = "No se encontró información relevante en la AEP."
    
    return llm_text


def generar_post(tema_post: str, llm_text: str) -> str:
    prompt = f"""
Rol:
Eres un Community Manager experto en comunicación en salud pediátrica. Gestionas una cuenta de redes sociales llamada Pediaclick, que utiliza dos personajes:
- SuperVita: superhéroe de Playmobil.
- Pediatra Chus: pediatra de Playmobil.

Objetivo:
Crea el texto de un post informativo sobre {tema_post}. El contenido debe:
- Estar dirigido a padres y madres.
- Ser tranquilizador, claro y empático.
- Basarse en las recomendaciones de la Asociación Española de Pediatría (AEP).
- Mantener un tono cercano y educativo, evitando tecnicismos innecesarios.
- Integrar de forma natural a SuperVita y a la pediatra Chus dentro de la narrativa.

Formato del post:
- Inicio llamativo.
- Cuerpo con pautas claras.
- Cierre con mensaje tranquilizador y llamada a la acción.
- Emojis moderados.
- 3–5 hashtags.
- Extensión 120–180 palabras.
- Nota: “Este contenido es informativo y no sustituye la valoración médica”.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def generar_prompt_imagen(texto_post: str) -> str:
    prompt_imagen = f"""
Eres un diseñador de prompts para modelos generadores de imágenes.

Objetivo:
A partir del siguiente post, crea un prompt visual para generar una imagen que lo acompañe en redes sociales.

Post:
{text_post}

Instrucciones para el prompt:
- Representar a los personajes **SuperVita (superhéroe de Playmobil)** y **Pediatra Chus (pediatra de Playmobil)**.
- Escena en estilo ilustración realista tipo juguete Playmobil.
- La imagen debe reflejar el mensaje principal del post de forma clara y positiva.
- Tono: cercano, educativo y tranquilizador.
- No inventar datos médicos.
- Usar exactamente el mismo estilo y personajes que en estos ejemplos (concatenar referencias aquí):
  [EjemploImagen1_URL]
  [EjemploImagen2_URL]
  [EjemploImagen3_URL]

Formato:
- Prompt conciso pero descriptivo (ideal para modelos tipo DALL·E o Stable Diffusion).
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_imagen}]
    )
    return response.choices[0].message.content


#########################################################################################################################
# INTERFAZ STREAMLIT
#########################################################################################################################

st.set_page_config(page_title="pedIAclick", page_icon="👶", layout="centered")

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
            llm_text = buscar_info_brave(tema_post)
        
        with st.spinner("✍️ Creando post con GPT..."):
            try:
                post = generar_post(tema_post, llm_text)
                st.session_state.post_generado = post
            except Exception as e:
                st.error(f"⚠️ Error al generar el post con GPT: {e}")
                st.session_state.post_generado = None
        
        if st.session_state.post_generado:
            st.subheader("📌 Post generado:")
            st.write(st.session_state.post_generado)

# Si ya hay post generado, mostrar botón para imagen
if st.session_state.post_generado:
    if st.button("🎨 Generar imagen del post"):
        with st.spinner("🖼️ Creando prompt para imagen..."):
            try:
                prompt_img = generar_prompt_imagen(st.session_state.post_generado)
                st.subheader("🎯 Prompt para generar la imagen:")
                st.code(prompt_img, language="markdown")
            except Exception as e:
                st.error(f"⚠️ Error al generar el prompt de imagen: {e}")
