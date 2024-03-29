"""
Code principal de l'application web Distribuco qui permet de gérer les requêtes et de les traiter
"""

from flask import render_template, request, redirect, Blueprint
from app.auth import login_is_required
import json
app_bp = Blueprint('app', __name__)
import pyotp
from dotenv import load_dotenv
import os
from app.auth import auth_session

load_dotenv() # Charger le fichier d'environnement

TOTP_SECRET = os.getenv("TOTP_SECRET") # Récupérer le secret TOPT

@app_bp.route('/') # Page d'accueil
def drinkMenu():
    """
    Fonction qui permet d'accéder à la page de connexion du site distribuco

    :param: Aucun(s)
    :return: Une redirection vers la page de connexion
    """
    return render_template('loginPage.jinja')

@app_bp.route('/app') # Page sécurisée
@login_is_required
def Secure_App():
    """
    Fonction qui permet d'accéder à la page principale sécurisée (avec authentification) du site
    Elle utilise le décorateur @login_is_required qui permet de ne laisser que les personnes authentifé d'accéder à la page web
    
    :param: Aucun(s)
    :return: Une redirection vers la page de création des boissons
    """
    with open("storage/drinks.json", "r") as f:
        drinks = json.load(f)
    return render_template('drinkMenu.jinja', drinks=drinks)

@login_is_required
@app_bp.route('/link-card') # Page sécurisée
def link_card():
    return render_template('linkCard.jinja')

@login_is_required
@app_bp.route('/admin-menu') # Page sécurisée
def admin_menu():
    with open("storage/ingredients.json", "r") as f:
        ingredients = json.load(f)
    return render_template('adminMenu.jinja', ingredients=ingredients)

@login_is_required
@app_bp.route('/delete_drink/<drink_index>', methods=['POST']) # Page sécurisée
def deleteDrink(drink_index):
    with open("storage/drinks.json", "r") as f:
        drinks = json.load(f)

    drinks.pop(int(drink_index))

    with open("storage/drinks.json", "w") as f:
        json.dump(drinks, f)

    return redirect('/app') # retourner à la page principale

def get_json_drinks(card_id=None, google_id=None):
    with open('storage/profiles.json') as f:
        profiles = json.load(f)

    for profile in profiles:
        if card_id and 'card_id' in profile and profile['card_id'] == card_id:
            return profile['drinks']
        elif google_id and 'google_id' in profile and profile['google_id'] == google_id:
            return profile['drinks']

    return None

@login_is_required
@app_bp.route('/card_id/<card_id>', methods=['GET']) # Page sécurisée
def storeCardId(card_id):
    with open("storage/profiles.json", "r") as f:
        profiles = json.load(f)

    profiles[0]["temp_card_id"] = card_id
    
    with open("storage/profiles.json", "w") as f:
        json.dump(profiles, f)

    return "SUCESS"

@login_is_required
@app_bp.route('/verifyOTP', methods=['POST']) # Page sécurisée
def verifyOTP():
    # Récupérer les numéros totp
    totp1 = request.form['totp1']
    totp2 = request.form['totp2']
    totp3 = request.form['totp3']
    totp4 = request.form['totp4']
    totp5 = request.form['totp5']
    totp6 = request.form['totp6']

    # Création d'un object topt (Time-based One Time Password) avec un secret en base 32
    totp = pyotp.TOTP(TOTP_SECRET, interval=60)

    # Concaténer les numéros totp en un seul
    user_totp = totp1 + totp2 + totp3 + totp4 + totp5 + totp6

    print(user_totp, TOTP_SECRET)

    # Valider le code totp
    totp_validation = totp.verify(user_totp)

    if totp_validation:
        with open("storage/profiles.json", "r") as f:
            profiles = json.load(f)

        new_profile = {
            "card_id": profiles[0]["temp_card_id"],
            "email": auth_session["google_id"]
        }
        profiles.append(new_profile)

        with open("storage/profiles.json", "w") as f:
            json.dump(profiles, f)
    else:
        print("Erreur de validation OTP")

    return redirect('/app') # retourner à la page principale

@login_is_required
@app_bp.route('/get-drinks/<card_id>', methods=['GET'])
def get_drinks(card_id):
    return(get_json_drinks(card_id, None))

@login_is_required
@app_bp.route('/ajout')
def ajout():
    """
    Fonction qui permet d'accéder à la page de création des boissons

    :param: Aucun(s)
    :return: Une redirection vers la page de création des boissons
    """
    with open("storage/ingredients.json", "r") as f:
        ingredients = json.load(f)
    return render_template('ajout.jinja', ingredients=ingredients)

@login_is_required
@app_bp.route('/creation-boisson', methods=['POST'])
def creation_boisson():
    """
    Fonction qui permet l'envoi du formulaire pour créer une boisson

    :param: Aucun(s)
    :return: Une redirection vers la page principale (sécurisée) du site
    """

    # Récupérer les données du formulaire
    nom_boisson = request.form['nom']

    # Quantite de liquide pour chaque pompe
    boisson_ml_1 = request.form['boisson_ml_1']
    boisson_ml_2 = request.form['boisson_ml_2']
    boisson_ml_3 = request.form['boisson_ml_3']
    boisson_ml_4 = request.form['boisson_ml_4']

    volumeTotal = request.form['total']

    couleur = request.form['couleur']

    # Récupérer les données du JSON
    with open('storage/drinks.json', 'r') as f:
        data = json.load(f)

    # Création des nouvelles données
    new_data = {
        "name": nom_boisson,
        "drink":{
            "volumeTotal": volumeTotal,
            "boisson_ml_1": boisson_ml_1,
            "boisson_ml_2": boisson_ml_2,
            "boisson_ml_3": boisson_ml_3,
            "boisson_ml_4": boisson_ml_4,
        },
        "couleur": couleur
    }
    data.append(new_data)

    # ÉCriture des nouvelles données
    with open('storage/drinks.json', 'w') as f:
        json.dump(data, f)

    return redirect('/app') # retour à l'application

