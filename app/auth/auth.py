# Code copié et modifié d'ici:
# 
# https://github.com/code-specialist/flask_google_login

import os
import pathlib
import json
import requests
from flask import session, abort, redirect, request, render_template, Blueprint
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from dotenv import load_dotenv

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
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # ERREUR 401: Si l'utilisateur n'est pas connecté
        else:
            return function()
    return wrapper


@auth_bp.route("/connexion") # réponse de l'authentification
def connexion():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth_bp.route("/callback")
def callback():
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


@auth_bp.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect("/")