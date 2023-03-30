from flask import render_template, request, redirect, Blueprint
from app.auth import login_is_required
import json
app_bp = Blueprint('app', __name__)

@app_bp.route('/') # Page d'accueil
def drinkMenu():
    return render_template('loginPage.jinja')

@app_bp.route('/app') # Page sécurisée
@login_is_required
def Secure_App():
    with open("storage/drinks.json", "r") as f:
        drinks = json.load(f)
    return render_template('drinkMenu.jinja', drinks=drinks)

@app_bp.route('/link-card') # Page sécurisée
def link_card():
    return render_template('linkCard.jinja')

@app_bp.route('/get-drinks')
def get_drinks():
    with open("storage/drinks.json", "r") as f:
        drinks = json.load(f)
    return(drinks)

@app_bp.route('/ajout')
def ajout():
    """
    Fonction qui permet d'accéder à la page de création des boissons

    :param: Aucun(s)
    :return: Une redirection à la de création de boissons
    """
    with open("storage/ingredients.json", "r") as f:
        ingredients = json.load(f)
    return render_template('ajout.jinja', ingredients=ingredients)

@app_bp.route('/creation-boisson', methods=['POST'])
def creation_boisson():
    """
    Fonction qui permet l'envoi du formulaire pour créer une boisson

    :param: Aucun(s)
    :return: Une redirection à la page principale du site
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

