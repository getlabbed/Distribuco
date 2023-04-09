"""
Ceci est le module principal de l'application web Distribuco

Il contient tout le code nécéssaire afin de faire fonctionner le site web: https://distribuco.ca
"""
from flask import Flask
from .app import app_bp
from .auth.auth import auth_bp
from .auth.auth import client_secrets_file
import json

# Importation pour la documentation Sphinx
from .app import *

def create_app():
    """
    Créé l'instance de l'application distribuco

    :param: Aucun(s)
    :return: l'instance de l'application
    """

    app = Flask(__name__)

    with open(client_secrets_file, 'r') as f:
        data = json.load(f)

    app.secret_key = data['web']['client_secret']
    app.register_blueprint(auth_bp)
    app.register_blueprint(app_bp)
    return app