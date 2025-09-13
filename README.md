# PediatrIA

El proyecto **pedIAtria** es una aplicación diseñada para asistir en la práctica pediátrica mediante el uso de inteligencia artificial. 

Lo que se busca es la automatización de la publicación de contenido médico-pediátrico en redes sociales, facilitando la difusión de información 
relevante y actualizada para profesionales de la salud y padres.

Para ello, se genera una interfaz de usuario interactiva utilizando Streamlit, que permite a los profesionales de la salud ingresar casuísticas
y recibir imágenes representativas de las mismas, generadas por modelos de inteligencia artificial como DALL-E.

Posteriormente, y previa validación del contenido por parte de un profesional, se programa la publicación automática de estas imágenes junto con textos explicativos.

Esta documentación proporciona una visión general del proyecto, su estructura y cómo utilizar sus componentes principales.


```bash
pedIAtria/
 ├─ streamlit/
 │    ├─ app.py
 │    ├─ pedIAclick.py
 └─ Docs/
      └─ source/
          └─ conf.py
```

Para la generación de la documentación:

1. Descargar la plantilla html corresponiente `html_theme = 'sphinx_rtd_theme'`
2. Ir a la carpeta Docs/
3. ejecutar en terminal `make html` 

Para abrir la documentación, ejecutar en terminal: start build\html\index.html
