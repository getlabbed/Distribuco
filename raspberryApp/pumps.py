import RPi.GPIO as gpio
import time
from threading import Thread
import socketio
sio = socketio.Client() # Création du client socketIO

PUMP_PINS = [[20, 21], [16, 12], [8, 25], [24, 23]]  # Pompe 1, Pompe 2, Pompe 3, Pompe 4
PRESSURE_SENSOR_PIN = 7
FLOW_RATE = 400  # 400 ml/min

def init():
    print("Initialisation des pins")
    gpio.setmode(gpio.BCM)
    for pins in PUMP_PINS:
        gpio.setup(pins[0], gpio.OUT)
        gpio.setup(pins[1], gpio.OUT)
    gpio.setup(PRESSURE_SENSOR_PIN, gpio.IN)

def start_pump(pump_id):
    print(f"Démarrage de la pompe {pump_id + 1}")
    gpio.output(PUMP_PINS[pump_id][0], False)
    gpio.output(PUMP_PINS[pump_id][1], True)

def stop_pump(pump_id):
    gpio.output(PUMP_PINS[pump_id][0], False)
    gpio.output(PUMP_PINS[pump_id][1], False)

def pressure_sensor_triggered():
    print("Détecteur de pression activé")
    """
    Fonction qui détecte si le capteur de pression est activé

    :param 0: Aucun(s)
    :return: True, si le capteur de pression est activé, False sinon
    :rtype: booléen
    """
    return gpio.input(PRESSURE_SENSOR_PIN)

def pump_liquid(pump_id, ml_to_pump):
    print(f"Pompe {pump_id + 1} en cours")
    """
    Fonction qui pompe la quantité de liquide spécifiée à la vitesse spécifiée

    :param pump_id: Index de la pompe à pomper
    :param ml_to_pump: Quantité de liquide à pomper (ml)
    :return: Rien
    """
    print(f"Pompe {pump_id + 1} en cours")
    flow_rate_seconds = FLOW_RATE / 60  # ml/s
    pumping_time = ml_to_pump / flow_rate_seconds
    start_time = time.time()

    while (time.time() - start_time < pumping_time) and pressure_sensor_triggered():
        start_pump(pump_id)
        time.sleep(0.1)

    stop_pump(pump_id)
    print(f"Pompe {pump_id + 1} arrêtée")

init()

def pumping_thread(pump_amounts):
    """
    Fonction qui gère les thread de pompage des liquides

    :param pump_amounts: Liste des quantités de liquide à pomper (ml)
    :return: Rien
    """
    try:
        while not pump_complete:
            if pressure_sensor_triggered() and pump_flag:
            
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
        gpio.cleanup()

# Fonction qui est appelée lorsque le serveur socketIO envoie un évènement 'start_pump'
@sio.on('start_pump')
def start_pumpssssss(data):
    global pump_flag
    print("socketIO: start_pump")
    pump_amounts = data['pump_amounts']
    hardware_thread = Thread(target=pumping_thread, args=(pump_amounts,))
    hardware_thread.start()

def connect_socketio():
    connected = False # État de la connexion
    while not connected:
        try:
            # Connection locale au serveur socketIO
            sio.connect('http://0.0.0.0:5000')
            connected = True
        except Exception as e:
            print("ERREUR SOCKETIO POMPES:", e)
            time.sleep(5)

def main():
    connect_socketio() # Connexion au serveur socketIO
    
if __name__ == "__main__":
    main()