# Code copié et modifié d'ici:
# 
# https://github.com/code-specialist/flask_google_login

import os
import pathlib
import json
import requests
from flask import session, abort, redirect, request, Blueprint
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

auth_bp = Blueprint('auth', __name__) # Compartimentalisation de l'application

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

with open(client_secrets_file, 'r') as f:
    data = json.load(f)

CLIENT_ID = data['web']['client_id']

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://distribuco.ca/callback"
)


def login_is_required(function):
    """
    Fonction qui permet de bloquer ou non l'exécution d'une fonction dépendamment 
    Elle contient un wrapper qui permet d'étendre la fonctionnalité d'une autre fonction (dans ce cas-ci un fonction dans app.py)
    
    :param 0: fonction à bloquer
    :return: la fonction wrappée
    """
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # ERREUR 401: Si l'utilisateur n'est pas connecté
        else:
            return function()
    return wrapper


@auth_bp.route("/login") # réponse de l'authentification
def login():
    """
    Fonction qui permet à l'utilisateur de se connecter à google lorsqu'il va sur /login
    
    :param 0: Aucun
    :return: une redirection vers l'URL de redirection qui est stocké dans client_secret.json
    """
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth_bp.route("/callback")
def callback():
    """
    Fonction qui permet de récupérer les informations sur la connexion Google

    :param 0: Aucun
    :return: une redirection vers l'application web sécurisée (/app)
    """
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # ERREUR 500: l'état n'est pas le même

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/app")


@auth_bp.route("/logout")
def logout():
    """
    Fonction qui permet à l'utilisateur de se déconnecter de google, en effacant les données de connexion.
    
    :param 0: Aucun
    :return: une redirection vers la page de connexion
    """
    session.clear()
    return redirect("/")