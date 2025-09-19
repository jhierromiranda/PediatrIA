import os
import subprocess
import requests
import base64

def guardar_post(texto_post, tema_post):
    """
    Guarda un post en un archivo de texto en la carpeta "backups" con el nombre "post_<tema_post>.txt".

    Parameters:
    texto_post (str): Texto del post a guardar.
    tema_post (str): Tema del post a guardar.

    Returns:
    str: Nombre del archivo en el que se guardó el post.
    """
    os.makedirs("backups", exist_ok=True)
    nombre_archivo = f"backups/post_{tema_post.replace(' ', '_')}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(texto_post)
    return nombre_archivo 


def guardar_imagen(image_result, tema_post):
    """
    Guarda una imagen en un archivo de imagen en la carpeta "backups" con el nombre "imagen_<tema_post>.png".

    Parameters:
    image_result (str or bytes): Imagen a guardar. Puede ser una URL o una imagen codificada en base64.
    tema_post (str): Tema del post a guardar.
    """

    os.makedirs("backups", exist_ok=True)
    nombre_archivo = f"backups/imagen_{tema_post.replace(' ', '_')}.png"
    
    if isinstance(image_result, str) and image_result.startswith("http"):
        # Si es URL, la descargamos
        img_data = requests.get(image_result).content
        with open(nombre_archivo, "wb") as f:
            f.write(img_data)
    else:
        # Si es base64
        with open(nombre_archivo, "wb") as f:
            f.write(image_result)


def git_commit_push(archivo):
    """
    Realiza un commit y push de un archivo en el repositorio de git.

    Parameters:
    archivo (str): Ruta del archivo a commitear y push.
    """

    subprocess.run(["git", "add", archivo], check=True)
    subprocess.run(["git", "commit", "-m", f"Backup {archivo}"], check=True)
    subprocess.run(["git", "push"], check=True)