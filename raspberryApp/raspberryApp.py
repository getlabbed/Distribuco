from flask import render_template, request, redirect, Blueprint, jsonify
import requests
import json
import pyotp
from . import socketio
from flask_socketio import emit
from dotenv import load_dotenv
import os

load_dotenv() # Charger le fichier d'environnement

TOTP_SECRET = os.getenv("TOTP_SECRET") # Récupérer le secret TOPT

raspberryApp_bp = Blueprint('app', __name__)

def str_round(input):
    float_input = float(input)
    output = round(float_input)
    return output

@raspberryApp_bp.route('/rfid_socketio') # Communication SocketIO
def rfid_socketio():
    # Envoyer la valeur RFID
    RFID = "123456"
    return {'status': 'success', 'message': RFID}

@raspberryApp_bp.route('/pumps', methods=['POST']) # Communication SocketIO
def pumps():

    # Quantite de liquide pour chaque pompe
    pump_1 = str_round(request.form['pump-1'])
    pump_2 = str_round(request.form['pump-2'])
    pump_3 = str_round(request.form['pump-3'])
    pump_4 = str_round(request.form['pump-4'])

    print(pump_1, pump_2, pump_3, pump_4)

    socketio.emit('start_pump', {'pump_amounts': [pump_1, pump_2, pump_3, pump_4], 'pump_ids': [1, 2, 3, 4]})
    return redirect('/drinkcomplete') # retourner à la page principale

@socketio.on('rfid_code') # Réception des données RFID via socketIO
def handle_rfid_data(data):
    print(f'Valeur RFID: {data}')
    emit('navigate', '/app', broadcast=True) # Redirection vers l'application principale

@socketio.on('pump_complete') # Réception des données RFID via socketIO
def handle_pump_complete():
    emit('navigate', '/', broadcast=True) # Redirection vers l'application principale

# Le thread de socketIO (keypad) vient envoyer au serveur qui lui renvoie la donnée au client
@socketio.on('keypad') # Réception des données KEYPAD via socketIO
def keypad(data):
    print(f'Valeur keypad: {data}')
    emit('keypad', data, broadcast=True) # Redirection vers la page de OTP

@raspberryApp_bp.route('/') # Page d'accueil
def drinkMenu():
    return render_template('welcomePage.jinja')

@raspberryApp_bp.route('/drinkcomplete') # Page d'accueil
def drinkComplete():
    return render_template('drinkPumping.jinja')

@raspberryApp_bp.route('/otp-link') # Page d'accueil
def otp_link():
    return render_template('OTPlinking.jinja')

@raspberryApp_bp.route('/get-otp-code')
def get_otp_code():
    # Création d'un object topt (Time-based One Time Password) avec un secret en base 32
    totp = pyotp.TOTP(TOTP_SECRET, interval=60)
    return jsonify({"otp_code": totp.now()})

# Page principale
@raspberryApp_bp.route('/app')
def Secure_App():
    response = requests.get('https://distribuco.ca/get-drinks')
    drinks = response.json()
    return render_template('drinkMenu.jinja', drinks=drinks)