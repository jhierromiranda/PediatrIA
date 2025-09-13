import streamlit as st
import requests
from openai import OpenAI
import os

# Leer claves desde st.secrets (no desde el repo)
BRAVE_TOKEN = st.secrets.get("BRAVE_TOKEN", "")
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")

# Ejemplo: mostrar input y botón (tu código original será más largo)
st.title("pedIAclick — generador de posts")
tema = st.text_input("Tema del post")
if st.button("Generar"):
    st.write("Aquí iría la llamada a Brave + GPT usando las claves de st.secrets")
