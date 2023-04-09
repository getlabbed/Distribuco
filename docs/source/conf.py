# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# Documentation pour la documentation du code source
# https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html

import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))

# importer les modules à documenter
from app import *
from raspberryApp import *

project = 'Distribuco'
copyright = '2023, Yanick Labelle'
author = 'Yanick Labelle'
release = '2023'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
   'sphinx.ext.duration',
   'sphinx.ext.doctest',
   'sphinx.ext.autodoc',
   'sphinx.ext.autosummary',
   'sphinx.ext.napoleon',
   'sphinx_jinja',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Permet d'enlever une erreur de compilation de la documentation
# Puisque ce module ne peut pas être importé ailleurs que sur un Raspberry Pi
autodoc_mock_imports = ["RPi"] # https://stackoverflow.com/a/56918885
