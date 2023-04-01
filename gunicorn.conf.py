"""
    Fichier de configuration gunicorn, permet d'accéder au variables d'environnement (.env)
    Ce fichier est nécessaire afin de faire fonctionner le système totp sur le serveur
    https://stackoverflow.com/a/68662906
"""

import os
from dotenv import load_dotenv

for env_file in ('.env'):
    env = os.path.join(os.getcwd(), env_file)
    if os.path.exists(env):
        load_dotenv(env)