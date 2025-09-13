#########################################################################################################################
##################################################### pedIAclick ########################################################
#########################################################################################################################
############################################## Fecha de creación: 20250911 ##############################################
############################################ Fecha de modificación: 20250911 ############################################
############################################# Autores: Jorge Hierro Francoy #############################################
#############################################      y Javier Miranda Pascual #############################################
#########################################################################################################################


#########################################################################################################################
######################################################## LIBRERÍAS ######################################################
#########################################################################################################################
import requests
import google.generativeai as genai
from openai import OpenAI
import os
import ast



#########################################################################################################################
# Parte 1: EXTRACCIÓN DE INFORMACION DE LA PÁGINA WEB DE LA ASOCIACIÓN ESPAÑOLA DE PEDIATRIA A TRAVÉS DE LA API DE BRAVE
#########################################################################################################################


# Cogemos el tema indicado como input (de momento lo hacemos a mano)
tema_post = 'Consumo de fruta en bebés'


# Parámetros y keys para la llamada a la API
url = 'https://api.search.brave.com/res/v1/web/search'
token = TOKEN
query = f'site:aeped.es {tema_post}'

# Headers de la consulta
headers = {
"Accept": "application/json",
"Accept-Encoding": "gzip",
"x-subscription-token": token
}

# Parámetros de la consulta
params = {
    'q': query,
    "extra_snippets": "true"
}


# Llamada a Brave
response = requests.get(url,  headers = headers, params = params).json()


# Recolectamos resultados
if 'results' in response['web'] and len(response['web']['results']) > 0:
    llm_text = ""
    llm_text += f'{query}. '
    for j in range(len(response['web']['results'])):
        if 'extra_snippets' in response['web']['results'][j]:
            llm_text += f"Descripcion {j+1}: {response['web']['results'][j]['title']} {response['web']['results'][j]['extra_snippets']}. "
        else:
            llm_text += f"Descripcion {j+1}: {response['web']['results'][j]['title']}. "




#########################################################################################################################
# Parte 2: CONEXION CON EL LLM
#########################################################################################################################

# Prompt:

prompt  = f"""
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
- Cuerpo: pautas breves sobre cómo actuar ante heridas deportivas en niños (qué hacer y qué evitar).
- Cierre: mensaje tranquilizador + llamada a la acción (p. ej., “Guarda este post” o “Consulta con tu pediatra”).
- Incluye emojis con moderación (2–4) y 3–5 hashtags relevantes.
- Extensión orientativa: 120–180 palabras.
- Añade la nota: “Este contenido es informativo y no sustituye la valoración médica”.

Restricciones y estilo:
- No inventes datos médicos; si falta información, recomienda consultar la web oficial de la AEP.
- Evita lenguaje alarmista; prioriza la tranquilidad y la claridad.

Información adicional (usa solo si es relevante; puede contener partes no relacionadas con el tema):
{llm_text}

Ejemplos de estilo (inspírate en tono, estructura y hashtags):

Ejemplo 1:
"27 de mayo | Día Nacional del Celíaco
Vivir sin gluten no es una limitación, es una forma diferente —y saludable— de alimentarse para nuestros pequeños con enfermedad celíaca.
Con un diagnóstico precoz y una dieta sin gluten estricta, los niños celíacos crecen sanos, felices... y fuertes como SuperVita.
Acompañarles desde la comprensión y el conocimiento es la mejor, hoy recordamos que comer diferente también es comer bien.
@Pediaclick @vithas @chusiffer
#DíaNacionalDelCelíaco #SinGlutenConSalud #vivirparacuidarte #pediatría #Pediaclick #supervita"

Ejemplo 2:
"Hoy, en el Día de la Esclerosis Tuberosa, queremos mandar un abrazo inmenso a todas las familias y a esos pequeños héroes que luchan cada día con una sonrisa.
La Esclerosis Tuberosa es una enfermedad genética rara que provoca el crecimiento de tumores benignos en diferentes órganos, pudiendo causar en niños problemas de desarrollo, convulsiones y dificultades en el aprendizaje. Recordemos la importancia del diagnóstico temprano, del apoyo familiar y de los avances médicos que cada día nos acercan más a mejorar la calidad de vida de estos niños y de sus familias.
#EsclerosisTuberosa #SaludInfantil #Pediaclick #SuperVita #Pediatría"

Ejemplo 3:
"¿Cómo saber si mi hijo está preparado para comenzar a comer otras cosas distintas a la leche? La pregunta del millón!!!
El reflejo de extrusión es un reflejo que tienen los lactantes para expulsar con la lengua alimentos distintos a la leche y que desaparece a partir de los 4-5 meses de vida. Si ha desaparecido, es uno de los signos de que tu hijo puede estar preparado... pero siempre haz caso a tu pediatra.
#alimentacionconsentidocomun #cadaniñoesdiferente #consultacontupediatra #supervita #Pediaclick"
"""

# Parámetro para llamar a uno u otro cuando se ejecute el código
gemini = 0
GPT = 1

# Gemini:
if gemini == 1:
    genai.configure(api_key="API_KEY")
    model = genai.GenerativeModel('gemini-1.5-flash')        
    response_gemini = model.generate_content(prompt).text

if GPT == 1:
    client = OpenAI(api_key = KEY)
    response_gtp = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content


# Next steps:
# 1. Añadir logs.
# 2. Almacenar los resultados de la llamada a la API (para no llamar dos veces por lo mismo)
# 3. Valorar resultados, ver si reducimos el número de webs extraídas (tanto por coste como por rendimiento)
# 4. Elección de modelo final y mejora de prompt si es necesario
