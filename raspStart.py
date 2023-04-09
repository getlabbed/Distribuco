from raspberryApp import create_app, socketio

from threading import Thread

from raspberryApp.rfid import main as rfidMain
from raspberryApp.pumps import main as pumpsMain

raspberryApp = create_app()

def main():
    # Mettre les codes du hardware dans un autre thread
    hardware_thread = Thread(target=rfidMain)
    hardware_thread = Thread(target=pumpsMain)
    hardware_thread.start()
    
    socketio.run(raspberryApp, port=5000, host="0.0.0.0", debug=True)

if __name__ == "__main__":
    main()