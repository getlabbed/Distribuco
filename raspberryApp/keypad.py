#! /usr/bin/env python3

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # Mode BCM

# Définir les broches du clavier numérique
ROWS = [9, 10, 22, 27]
COLS = [17, 4, 3, 2]

# Définir la disposition du clavier numérique
keys = [
    ['1', '2', '3', 'UP'],
    ['4', '5', '6', 'DWN'],
    ['7', '8', '9', '2nd'],
    ['CLR', '0', 'HLP', 'NTR']
]

# Définir les rangées en entrée (avec résistances de pull-up)
for row in ROWS:
    GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Définir les colonnes en sortie
for col in COLS:
    GPIO.setup(col, GPIO.OUT)
    GPIO.output(col, 1)

# Lire le clavier
try:
    while True:
        for col in range(4):
            GPIO.output(COLS[col], 0)
            for row in range(4):
                if GPIO.input(ROWS[row]) == 0:
                    print(keys[row][col])
                    time.sleep(0.2)
            GPIO.output(COLS[col], 1)
except:
    print("Erreur lors de la lecture du clavier 4x4")
finally: # Éxécuter peu importe s'il y a une erreur ou non
    GPIO.cleanup()