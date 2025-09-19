#########################################################################################################################
##################################################### pedIAclick ########################################################
#########################################################################################################################
import requests
import streamlit as st
from openai import OpenAI
import base64


#########################################################################################################################
# CONFIG
#########################################################################################################################
BRAVE_TOKEN = st.secrets.get("BRAVE_TOKEN", "")
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
OPENAI_KEY_IMAGES = st.secrets.get("OPENAI_API_KEY_IMAGES", "")

client = OpenAI(api_key=OPENAI_KEY)
client_images = OpenAI(api_key=OPENAI_KEY_IMAGES)


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


def generar_prompt_imagen(texto_post: str, imagen_ref: str) -> str:
    prompt_imagen = f"""
Crea una escena nueva basada en el tema: 'Deporte en el primer año de vida'. Asegúrate de que los personajes SuperVita y Pediatra Chus sean exactamente iguales a los de la imagen.
"""
    return prompt_imagen



def generar_imagen_dalle(prompt_img: str):
    try:
        with open("assets/referencia.jpeg", "rb") as f:
            response = client_images.images.edit(
            model="gpt-image-1",
            image=f,
            prompt=prompt_img,
            size="1024x1024"
            )
            
        image_obj = response.data[0]
        if image_obj.url:
            return image_obj.url
        elif image_obj.b64_json:
            return base64.b64decode(image_obj.b64_json)
        else:
            st.error("⚠️ La API no devolvió URL ni imagen base64.")
            return None
    except Exception as e:
        st.error(f"⚠️ Error al generar la imagen: {e}")
        return None


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
