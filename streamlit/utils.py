import os
import subprocess
import requests
import base64
from PIL import Image, ImageDraw, ImageFont

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

    subprocess.run(["git", "add", "backups/"], check=True)

    # Solo commitea si hay cambios en backups/
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "backups/"], text=True
    ).strip()

    if status:
        subprocess.run([
            "git", "-c", f"user.name={user_name}",
            "-c", f"user.email={user_email}",
            "commit", "-m", f"Backup {archivo}"
        ], check=True)
    else:
        print("⚠️ No hay cambios nuevos en backups/, solo se hará push.")

    # Push siempre (para enviar commits pendientes)
    origin = subprocess.check_output(
        ["git", "remote", "get-url", "origin"], text=True
    ).strip()

    if origin.startswith("https://"):
        auth_url = origin.replace("https://", f"https://{user_name}:{github_token}@")
    else:
        raise ValueError("El remoto no usa HTTPS")

    subprocess.run(["git", "push", auth_url], check=True)


def agregar_marca_agua(imagen, texto="@pediaclick", opacidad=180):
    """
    Agrega una marca de agua a una imagen y la guarda en un archivo diferente.

    Parameters:
        imagen_path (str): Ruta del archivo de la imagen a marcar.
        salida_path (str): Ruta del archivo donde se guardará la imagen con marca de agua.
        texto (str): Texto a escribir en la marca de agua.
        opacidad (int): Opacidad del texto (0-255). Por defecto, 180.

    Returns:
        None
    """

    
    # Crear capa transparente para la marca de agua
    txt_layer = Image.new("RGBA", imagen.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Fuente proporcional (5% de la altura de la imagen)
    try:
        fuente = ImageFont.truetype("arial.ttf", int(imagen.size[1] * 0.05))
    except:
        fuente = ImageFont.load_default()

    # Calcular posición centrada en la parte inferior
    bbox = draw.textbbox((0, 0), texto, font=fuente)
    ancho_texto = bbox[2] - bbox[0]
    alto_texto = bbox[3] - bbox[1]

    x = (imagen.size[0] - ancho_texto) // 2
    y = imagen.size[1] - alto_texto - 40  # margen inferior

    # Dibujar sombra (negra, semitransparente)
    draw.text((x+2, y+2), texto, font=fuente, fill=(0, 0, 0, 120))
    
    # Dibujar texto principal (blanco con opacidad)
    draw.text((x, y), texto, font=fuente, fill=(255, 255, 255, opacidad))

    # Combinar imagen original con la capa de texto
    imagen_final = Image.alpha_composite(imagen, txt_layer)

    # Guardar como JPG o PNG
    imagen_final = imagen_final.convert("RGB")
    
    return imagen_final

