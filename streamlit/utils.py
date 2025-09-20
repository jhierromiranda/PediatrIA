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


def git_commit_push(archivo, user_name,user_email, github_token):
    """
    Realiza un commit y push de un archivo en el repositorio de git.

    Parameters:
    archivo (str): Ruta del archivo a commitear y push.
    """

    subprocess.run(["git", "add", archivo], check=True)

    # Hacer commit (solo si hay cambios)
    status = subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
    if status:
        subprocess.run([
            "git", "-c", f"user.name={user_name}",
            "-c", f"user.email={user_email}",
            "commit", "-m", f"Backup {archivo}"
        ], check=True)
    else:
        print("⚠️ No hay cambios nuevos para commitear")

    # Siempre hacer push (para enviar commits pendientes)
    origin = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True).strip()
    if origin.startswith("https://"):
        auth_url = origin.replace("https://", f"https://{user_name}:{github_token}@")
    else:
        raise ValueError("El remoto no usa HTTPS")
    subprocess.run(["git", "push", auth_url], check=True)
