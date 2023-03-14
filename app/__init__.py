from flask import Flask
from .app import app_bp
from .auth.auth import auth_bp
from .auth.auth import client_secrets_file
import json


def create_app():
    app = Flask(__name__)

    with open(client_secrets_file, 'r') as f:
        data = json.load(f)

    app.secret_key = data['web']['client_secret']
    app.register_blueprint(auth_bp)
    app.register_blueprint(app_bp)
    return app