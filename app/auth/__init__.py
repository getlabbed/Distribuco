from .auth import auth_bp as bp
from .auth import login_is_required as lir
from .auth import client_secrets_file as csf

auth_bp = bp
login_is_required = lir
client_secrets_file = csf