# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pedIAtria'
copyright = '2025, Javier Miranda y Jorge Hierro'
author = 'Javier Miranda y Jorge Hierro'
release = '13/09/2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
sys.path.insert(0, os.path.abspath('../../streamlit'))  # ruta a tus módulos

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

# Opciones HTML
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

