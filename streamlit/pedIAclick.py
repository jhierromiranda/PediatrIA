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

#########################################################################################################################
# FUNCIONES AUXILIARES

def buscar_info_brave(tema_post: str, BRAVE_TOKEN) -> str:
    """Busca información en la web de la AEP usando Brave API y devuelve un texto resumen."""

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
    """Genera el post con GPT usando el prompt definido."""
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
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content