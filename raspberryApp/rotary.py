#! /usr/bin/env python3

from RPi import GPIO
from time import sleep


DEBOUNCE_TIME = 0.01
DT = 23  # GPIO 23
CLK = 25 # GPIO 25

GPIO.setmode(GPIO.BCM)

# R/sistances de pull-up
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

compteur = 0
CLKDernierEtat = GPIO.input(CLK)

try:
    while (True):
        CLKValeur = GPIO.input(CLK)
        DTValeur = GPIO.input(DT)

        if CLKValeur != CLKDernierEtat:      # Si la valeur à changé
            sleep(DEBOUNCE_TIME)             # Debounce
            if GPIO.input(CLK) == CLKValeur: # Double vérification (debouncing)
                if DTValeur == CLKValeur:    # Dépendamment de la direction
                    compteur += 1
                else:
                    compteur -= 1
                print (compteur)
            CLKDernierEtat = CLKValeur       # Changer la valeur de la dernière valeur
        
except:
    GPIO.cleanup() # Remet les GPIO à leur état par défaut