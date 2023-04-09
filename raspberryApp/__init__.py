from flask import Flask

from flask_socketio import SocketIO

socketio = SocketIO()

# Importation pour la documentation Sphinx
from .raspberryApp import *

def create_app():
    """
    Créé l'instance de l'application distribuco pour Raspberry Pi

    :param 0: Aucun(s)
    :return: l'instance de l'application
    """
    raspberryApp = Flask(__name__)
    
    """
    Permet d'éviter une importation circulaire,
    en le placant sous l'initialisation de raspberryApp,
    à l'intérieur de la fonction (merci chatGPT)
    """
    from .raspberryApp import raspberryApp_bp

    raspberryApp.register_blueprint(raspberryApp_bp)
    socketio.init_app(raspberryApp)
    return raspberryApp