#! /usr/bin/env python3

import socketio
import time
from threading import Thread


# RPI.GPIO est seulement disponible sur les raspberryPi,
# ce qui ne permet pas l'exécution du code pour tester le code sur un autre ordinateur
import RPi.GPIO as GPIO
import serial

sio = socketio.Client() # Création du client socketIO

BROCHE_ACTIVATION  = 18     # Broche BCM (GPIO 18)

PORT_SERIEL = '/dev/ttyS0'  # Localisation du port Sériel

# Initialisation des paramètres sériel
ser = serial.Serial(baudrate = 2400,
                    bytesize = serial.EIGHTBITS,
                    parity   = serial.PARITY_NONE,
                    port     = PORT_SERIEL,
                    stopbits = serial.STOPBITS_ONE,
                    timeout  = 1)

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

# l'ordre des broches GPIO est important !!
PUMP_PINS = [[21, 20], [16, 12], [25, 5], [24, 23]]  # Pompe 1, Pompe 2, Pompe 3, Pompe 4
PRESSURE_SENSOR_PIN = 7

# Les valeurs de calibration pourrait être récupérées par l'application dans une version ultérieure

# Facteur de calibration calculé en utilisant la formule suivante:
# (Volume voulu / volume acquis (premier test)) * (Volume voulu / volume acquis (deuxième test), à l'aide des valeurs de calibration du premier test)

pump_3_calibration = (100 / 75) * (100 / 125)
pump_4_calibration = (100 / 60) * (100 / 105)
pump_calibration = [1, 1, pump_3_calibration , pump_4_calibration]

CALIBRATION = (100 / 75) * (100 / 125) # Facteur de calibration
FLOW_RATE = 400  # 400 ml/min

pump_flag = True

keypad_enabled = False
rfid_enabled = True

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

for pins in PUMP_PINS:
    GPIO.setup(pins[0], GPIO.OUT)
    GPIO.setup(pins[1], GPIO.OUT)

    # Initialiser les broches de moteurs pour ne pas pomper (certaines broches sont à l'état haut au démarrage)
    GPIO.output(pins[0], False)
    GPIO.output(pins[1], False)

                 
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

def init():
    print("Initialisation des pins")
    GPIO.setmode(GPIO.BCM)
    for pins in PUMP_PINS:
        GPIO.setup(pins[0], GPIO.OUT)
        GPIO.setup(pins[1], GPIO.OUT)
    GPIO.setup(PRESSURE_SENSOR_PIN, GPIO.IN)

def start_pump(pump_id):
    GPIO.output(PUMP_PINS[pump_id][0], False)
    GPIO.output(PUMP_PINS[pump_id][1], True)

def stop_pump(pump_id):
    GPIO.output(PUMP_PINS[pump_id][0], False)
    GPIO.output(PUMP_PINS[pump_id][1], False)

def pressure_sensor_triggered():
    print("Détecteur de pression activé")
    """
    Fonction qui détecte si le capteur de pression est activé

    :param 0: Aucun(s)
    :return: True, si le capteur de pression est activé, False sinon
    :rtype: booléen
    """
    return GPIO.input(PRESSURE_SENSOR_PIN)

def pump_liquid(pump_id, ml_to_pump):
    print(f"Pompe {pump_id + 1} en cours")
    """
    Fonction qui pompe la quantité de liquide spécifiée à la vitesse spécifiée

    :param pump_id: Index de la pompe à pomper
    :param ml_to_pump: Quantité de liquide à pomper (ml)
    :return: Rien
    """
    flow_rate_seconds = FLOW_RATE / 60  # Conversion en ml/s

    pumping_time = (ml_to_pump * pump_calibration[pump_id-1]) / flow_rate_seconds
    start_time = time.time()
    time.sleep(0.5)

    while (time.time() - start_time < pumping_time) and pressure_sensor_triggered():
        start_pump(pump_id)
        time.sleep(0.1)

    stop_pump(pump_id)
    print(f"Pompe {pump_id + 1} arrêtée")

def pumping_thread(pump_amounts):
    """
    Fonction qui gère les thread de pompage des liquides

    :param pump_amounts: Liste des quantités de liquide à pomper (ml)
    :return: Rien
    """
    init() # Super important !!!
    pump_complete = False
    global pump_flag, rfid_enabled, keypad_enabled
    try:
        while not pump_complete:
            if pressure_sensor_triggered() and pump_flag:
                print("Pression détectée")
            
                # Commencer à pomper
                pump_flag = False
                pump_liquid_threads = []
                for i, amount in enumerate(pump_amounts):
                    pump_liquid_thread = Thread(target=pump_liquid, args=(i, amount))
                    pump_liquid_threads.append(pump_liquid_thread)
                    pump_liquid_thread.start()

                # Attendre que toutes les pompes aient fini de pomper
                for pump_liquid_thread in pump_liquid_threads:
                    pump_liquid_thread.join()

                print("Pompage complet")
                pump_complete = True
            else:
                print("Pas de pression")
                time.sleep(1)
    except KeyboardInterrupt:
        print("Interruption par l'utilisateur")
    finally:
        print("Nettoyage des pins")
        for i in range(len(PUMP_PINS)):
            stop_pump(i)
        sio.emit('pump_complete') # Évènement socketIO qui indique que le pompage est terminé
        pump_complete = False
        rfid_enabled = True
        keypad_enabled = False

# Fonction qui est appelée lorsque le serveur socketIO envoie un évènement 'start_pump'
@sio.on('start_pump')
def start_pumpssssss(data):
    global pump_flag, keypad_enabled, rfid_enabled
    pump_flag = True
    print("socketIO: start_pump")
    pump_amounts = data['pump_amounts']
    hardware_thread = Thread(target=pumping_thread, args=(pump_amounts,))
    hardware_thread.start()
    rfid_enabled = False
    keypad_enabled = True

def main():
    global rfid_enabled, keypad_enabled
    connected = False # État de la connexion
    while not connected:
        try:
            # Connection locale au serveur socketIO
            sio.connect('http://0.0.0.0:5000')
            connected = True
        except Exception as e:
            print("ERREUR SOCKETIO KEYPAD:", e)
            time.sleep(5)

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
            if rfid_enabled:
                if ser.in_waiting >= 12:     # Si 12 bits sont disponibles en entrée
                    rfid_code = ser.read(12) # Lire les 12 bits du port sériel
                    print(rfid_code)         # Ligne de débuggage

                    # Si le code est un code RFID Valide
                    if validate_rfid(rfid_code):
                        print("Read RFID code: ", rfid_code.decode('utf-8')) # Ligne de débuggage

                        # Envoyer le code RFID via socketIO
                        sio.emit('rfid_code', rfid_code.decode('utf-8')) # Évènement socketIO
                        
                        # Activer le clavier et désactiver le capteur RFID
                        rfid_enabled = False
                        keypad_enabled = True

                    ser.reset_input_buffer() # Réinitialiser le buffer d'entrée (évite les erreurs lors de la deuxième lecture)
                    time.sleep(2)

            if keypad_enabled:
                for col in range(4):
                    GPIO.output(COLS[col], 0)
                    for row in range(4):
                        if GPIO.input(ROWS[row]) == 0:
                            print(keys[row][col])
                            sio.emit('keypad', keys[row][col]) # Évènement socketIO
                            time.sleep(0.2)
                    GPIO.output(COLS[col], 1)
    except e:
        print("Erreur lors de la lecture du clavier 4x4", e)
        print("Erreur RFID:", e)
        print("Désactivation du capteur RFID...")
            
        # Désactivation du capteur RFID en cas d'erreur
        GPIO.output(BROCHE_ACTIVATION, GPIO.HIGH)

    finally: # Éxécuter peu importe s'il y a une erreur ou non
        GPIO.cleanup()

if __name__ == "__main__":
    main()