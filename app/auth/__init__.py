"""
Ceci est le sous module auth

Il contient le code nécéssaire à l'authentification d'un utilisateur par une connexion OAuth via Google
"""
from .auth import auth_bp as bp
from .auth import login_is_required as lir
from .auth import client_secrets_file as csf

auth_bp = bp
login_is_required = lir
client_secrets_file = csf