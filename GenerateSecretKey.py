"""
Programme permettant de générer un secret TOPT automatiquement
"""

import pyotp

TOTP_SECRET = pyotp.random_base32()

with open('app/.env', 'w') as file:
    file.write('TOTP_SECRET = ' + TOTP_SECRET)

with open('raspberryApp/.env', 'w') as file:
    file.write('TOTP_SECRET = ' + TOTP_SECRET)