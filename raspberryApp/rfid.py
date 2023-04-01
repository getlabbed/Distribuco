#! /usr/bin/env python3

import socketio

from time import sleep

sio = socketio.Client() # Création du client socketIO

# RPI.GPIO est seulement disponible sur les raspberryPi,
# ce qui ne permet pas l'exécution du code pour tester le code sur un autre ordinateur
import RPi.GPIO as GPIO
import serial

BROCHE_ACTIVATION  = 24     # Broche BCM (GPIO 24)

PORT_SERIEL = '/dev/ttyS0'  # Localisation du port Sériel
                  
def validate_rfid(code):
    """
    Fonction qui permet de valider un code RFID
    Un code RFID valide est:
        - 12 caractères de long
        - Le premier caractère est un charactère de saut de ligne
        - Le dernier caractère est un charactère de retour chariot
    :param 0: Le code RFID à valider
    :return 0: Le code RFID
    :return 1: Faux
    """

    s = code.decode("ascii")

    # Si le code est valide
    if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
        # Retourner le code RFID et enlever les charactères indésirables
        return s[1:-1]
    else:
        # Le code n'est pas valide
        return False

def main():
    """
    Fonction principale du programme RFID
    :param 0: Rien
    :return: Rien
    """
    connected = False # État de la connexion
    while not connected:
        try:
            # Connection locale au serveur socketIO
            sio.connect('http://0.0.0.0:5000')
            connected = True
        except Exception as e:
            print("ERREUR SOCKETIO RFID:", e)
            sleep(5)
    
    # Initialize the Raspberry Pi by quashing any warnings and telling it
    # we're going to use the BCM pin numbering scheme.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # This pin corresponds to GPIO1, which we'll use to turn the RFID
    # reader on and off with.
    GPIO.setup(BROCHE_ACTIVATION, GPIO.OUT)

    # Setting the pin to LOW will turn the reader on.  You should notice
    # the green LED light on the reader turn red if successfully enabled.

    print("Enabling RFID reader and reading from serial port: " + PORT_SERIEL)
    GPIO.output(BROCHE_ACTIVATION, GPIO.LOW)

    # Initialisation des paramètres sériel
    ser = serial.Serial(baudrate = 2400,
                        bytesize = serial.EIGHTBITS,
                        parity   = serial.PARITY_NONE,
                        port     = PORT_SERIEL,
                        stopbits = serial.STOPBITS_ONE,
                        timeout  = 1)

    try:
        while(True):
            rfid_code = ser.read(12) # Lire 12 bits du port sériel

            # Si le code est un code RFID Valide
            if validate_rfid(rfid_code):
                # Ligne de débuggage
                print("Read RFID code: ", rfid_code.decode('utf-8'))
                # Envoyer le code RFID via socketIO
                sio.emit('rfid_code', rfid_code.decode('utf-8')) # Évènement socketIO
            sleep(2)
    except Exception as e:
        print("Erreur RFID:", e)
        print("Désactivation du capteur RFID...")
        
        # Désactivation du capteur RFID en cas d'erreur
        GPIO.output(BROCHE_ACTIVATION, GPIO.HIGH)

    sio.disconnect() # Déconnexion du serveur socketIO, à la fin du script

        
if __name__ == "__main__":
    main()