from flask import render_template, request, redirect, Blueprint, jsonify
import json
import pyotp
from . import socketio
from flask_socketio import emit
from dotenv import load_dotenv
import os

load_dotenv() # Charger le fichier d'environnement

TOTP_SECRET = os.getenv("TOTP_SECRET") # Récupérer le secret TOPT

raspberryApp_bp = Blueprint('app', __name__)

@raspberryApp_bp.route('/rfid_socketio') # Communication SocketIO
def rfid_socketio():
    # Envoyer la valeur RFID
    RFID = "123456"
    return {'status': 'success', 'message': RFID}

@socketio.on('rfid_code') # Réception des données RFID via socketIO
def handle_rfid_data(data):
    print(f'Valeur RFID: {data}')
    emit('navigate', '/otp-link', broadcast=True) # Redirection vers la page de OTP

@raspberryApp_bp.route('/') # Page d'accueil
def drinkMenu():
    return render_template('welcomePage.jinja')

@raspberryApp_bp.route('/otp-link') # Page d'accueil
def otp_link():
    return render_template('OTPlinking.jinja')

@raspberryApp_bp.route('/get-otp-code')
def get_otp_code():
    # Création d'un object topt (Time-based One Time Password) avec un secret en base 32
    totp = pyotp.TOTP(TOTP_SECRET, interval=60)
    return jsonify({"otp_code": totp.now()})

@raspberryApp_bp.route('/app') # Page sécurisée
def Secure_App():
    with open("storage/drinks.json", "r") as f:
        drinks = json.load(f)
    return render_template('drinkMenu.jinja', drinks=drinks)

@raspberryApp_bp.route('/ajout') # Page de création des boissons
def ajout():
    with open("storage/ingredients.json", "r") as f:
        ingredients = json.load(f)
    return render_template('ajout.jinja', ingredients=ingredients)

@raspberryApp_bp.route('/creation-boisson', methods=['POST']) # Envoi du formulaire pour créer une boisson
def creation_boisson():
    # Récupérer les données du formulaire
    nom_boisson = request.form['nom']

    # % de chaque sliders
    boisson_1 = request.form['boisson_1']
    boisson_2 = request.form['boisson_2']
    boisson_3 = request.form['boisson_3']
    boisson_4 = request.form['boisson_4']

    # % cumulatif
    pourcentage_1 = request.form['pourcentage_1']
    pourcentage_2 = request.form['pourcentage_2']
    pourcentage_3 = request.form['pourcentage_3']
    pourcentage_4 = request.form['pourcentage_4']

    volumeTotal = request.form['total']


    # Récupérer les données du JSON
    with open('storage/drinks.json', 'r') as f:
        data = json.load(f)

    # Création des nouvelles données
    new_data = {
        "name": nom_boisson,
        "drink":{
            "volumeTotal": volumeTotal,
            "boisson1_s": boisson_1,
            "boisson2_s": boisson_2,
            "boisson3_s": boisson_3,
            "boisson4_s": boisson_4,
            "boisson1_p": pourcentage_1,
            "boisson2_p": pourcentage_2,
            "boisson3_p": pourcentage_3,
            "boisson4_p": pourcentage_4
        },
        "img": "placeholder.png",
        "link": "/boisson"
    }
    data.append(new_data)

    # ÉCriture des nouvelles données
    with open('storage/drinks.json', 'w') as f:
        json.dump(data, f)

    return redirect('/') # retourner à la page principale