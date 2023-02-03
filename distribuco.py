from flask import Flask, render_template, request, redirect
import json
app = Flask(__name__)

@app.route('/')
def drinkMenu():
    with open("storage/drinks.json", "r") as f:
        drinks = json.load(f)
    return render_template('drinkMenu.html', drinks=drinks)

@app.route('/rien')
def rien():
    return "BRUH"

@app.route('/ajout')
def ajout():
    with open("storage/ingredients.json", "r") as f:
        ingredients = json.load(f)
    return render_template('ajout.html', ingredients=ingredients)

@app.route('/creation-boisson', methods=['POST'])
def creation_boisson():
    # Récupérer les données du formulaire
    nom_boisson = request.form['nom']
    boisson_1 = request.form['boisson_1']
    boisson_2 = request.form['boisson_2']
    boisson_3 = request.form['boisson_3']
    boisson_4 = request.form['boisson_4']

    # Récupérer les données du JSON
    with open('storage/drinks.json', 'r') as f:
        data = json.load(f)

    # Création des nouvelles données
    new_data = {
        "name": nom_boisson,
        "img": "placeholder.png",
        "link": "/boisson"
    }
    data.append(new_data)

    # ÉCriture des nouvelles données
    with open('storage/drinks.json', 'w') as f:
        json.dump(data, f)

    return redirect('/') # retourner à la page principale

if __name__ == "__main__":
    app.run(debug=True)