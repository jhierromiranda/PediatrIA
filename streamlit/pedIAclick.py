#----------------------------
# Fecha de creación: 20250911 
# Fecha de modificación: 20250913
# Autores: 
# - Jorge Hierro Francoy 
# - Javier Miranda Pascual
#----------------------------

# LIBRERÍAS
import requests
import streamlit as st
from openai import OpenAI
import os
import base64

#########################################################################################################################
# FUNCIONES AUXILIARES

def buscar_info_brave(tema_post: str, BRAVE_TOKEN) -> str:
    """
    Busca información en la API de Brave asociada en la Asociación Española de Pediatría (AEP) para un tema dado.

    Args:
        tema_post (str): Tema sobre el que se busca información en la AEP. Lo introduce el usuario y puede ser cualquier tema relacionado con la pediatría.
        BRAVE_TOKEN (str): Token de subscripción para la API de Brave. Variable de entorno.

    Returns:
        str: Texto con la información asociada al tema en la AEP. Si no se encuentra información, devuelve un mensaje de error.
    """

    url = 'https://api.search.brave.com/res/v1/web/search'
    query = f'site:aeped.es {tema_post}'
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "x-subscription-token": BRAVE_TOKEN
    }
    params = {
        'q': query,
        "extra_snippets": "true"
    }
    
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

def generar_post(tema_post: str, llm_text: str, client) -> str:
    
    """
    Genera un post informativo para Pediaclick basado en la información asociada a un tema en la AEP.

    Args:
        tema_post (str): Tema sobre el que se busca información en la AEP. Lo introduce el usuario y puede ser cualquier tema relacionado con la pediatría.
        llm_text (str): Texto con la información asociada al tema en la AEP. Si no se encuentra información, devuelve un mensaje de error.
        client (OpenAI.Client): Cliente de la API de OpenAI, que se utiliza para generar el contenido del post.

    Returns:
        str: Texto del post informativo. Si no se pudo generar el post debido a la falta de información relevante en la AEP, devuelve un mensaje de error.
    """

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
- Inicio llamativo: una frase que capte la atención (pregunta o dato).
- Cuerpo: pautas breves sobre cómo actuar.
- Cierre: mensaje tranquilizador + llamada a la acción (p. ej., “Guarda este post” o “Consulta con tu pediatra”).
- Incluye emojis con moderación (2–4) y 3–5 hashtags relevantes.
- Extensión orientativa: 120–180 palabras.
- Añade la nota: “Este contenido es informativo y no sustituye la valoración médica”.

Restricciones y estilo:
- No inventes datos médicos; si falta información, recomienda consultar la web oficial de la AEP.
- Evita lenguaje alarmista; prioriza la tranquilidad y la claridad.

Información adicional (usa solo si es relevante; puede contener partes no relacionadas con el tema):
{llm_text}
"""
    if llm_text != "No se encontró información relevante en la AEP.":
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
    else:
        return "No se pudo generar el post debido a la falta de información relevante en la AEP."
    

def generar_prompt_imagen(texto_post: str, imagen_ref: str) -> str:
    prompt_imagen = f"""
Crea una escena nueva basada en el tema: '{texto_post}'. Asegúrate de que los personajes SuperVita y Pediatra Chus sean exactamente iguales a los de la imagen.
"""
    return prompt_imagen

def generar_imagen_dalle(prompt_img: str, client_images):
    try:
        with open("assets/referencia.jpeg", "rb") as f:
            response = client_images.images.edit(
            model="gpt-image-1",
            image=f,
            prompt=prompt_img,
            size="1024x1024",
            n=1
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
    
def generar_prompt_imagen(texto_post: str, imagen_ref: str) -> str:
    """Genera un prompt para una imagen basada en el texto del post y la imagen de referencia.

    Args:
        texto_post (str): Texto del post que se va a generar.
        imagen_ref (str): Imagen de referencia para la que se va a generar la escena.

    Returns:
        str: Prompt para generar la imagen.
    """

    prompt_imagen = f"""
Crea una escena nueva basada en el tema: 'Deporte en el primer año de vida'. Asegúrate de que los personajes SuperVita y Pediatra Chus sean exactamente iguales a los de la imagen.
"""
    return prompt_imagen


def generar_imagen_dalle(prompt_img: str, client_images):
    """Genera una imagen basada en el prompt y la imagen de referencia.

    Args:
        prompt_img (str): Prompt para generar la imagen.
        client_images (OpenAI): Cliente de la API de OpenAI para generar imágenes.

    Returns:
        str|bytes: URL de la imagen generada o imagen en base64 si la API devuelve una imagen base64.
    """
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
