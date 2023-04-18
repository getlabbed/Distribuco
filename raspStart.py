from raspberryApp import create_app, socketio

from threading import Thread

from raspberryApp.keypad_pumps_rfid import main as keypadPumpsRfidMain

raspberryApp = create_app()

def main():
    # Mettre les codes du hardware dans un autre thread
    hardware_thread = Thread(target=keypadPumpsRfidMain)
    hardware_thread.start()
    
    socketio.run(raspberryApp, port=5000, host="0.0.0.0", debug=True)

if __name__ == "__main__":
    main()