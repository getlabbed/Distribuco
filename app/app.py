from flask import render_template, request, redirect, Blueprint
from app.auth import login_is_required
import json
app_bp = Blueprint('app', __name__)
import pyotp
from dotenv import load_dotenv
import os

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
#DEV @login_is_required
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

#DEV @login_is_required
@app_bp.route('/link-card') # Page sécurisée
def link_card():
    return render_template('linkCard.jinja')

#DEV @login_is_required
@app_bp.route('/admin-menu') # Page sécurisée
def admin_menu():
    with open("storage/ingredients.json", "r") as f:
        ingredients = json.load(f)
    return render_template('adminMenu.jinja', ingredients=ingredients)

#DEV @login_is_required
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

    # Concaténer les numéro totp en un seul
    user_totp = totp1 + totp2 + totp3 + totp4 + totp5 + totp6

    # Valider le code totp
    totp_validation = totp.verify(user_totp)

    if totp_validation:
        pass # Envoyer une requête socketIO pour réccupérer le numéro de carte RFID
    else:
        pass # Ne rien faire

    return redirect('/app') # retourner à la page principale

#DEV @login_is_required
@app_bp.route('/get-drinks')
def get_drinks():
    with open("storage/drinks.json", "r") as f:
        drinks = json.load(f)
    return(drinks)

#DEV @login_is_required
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

#DEV @login_is_required
@app_bp.route('/creation-boisson', methods=['POST'])
def creation_boisson():
    """
    Fonction qui permet l'envoi du formulaire pour créer une boisson

    :param: Aucun(s)
    :return: Une redirection vers la page principale (sécurisée) du site
    """

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

