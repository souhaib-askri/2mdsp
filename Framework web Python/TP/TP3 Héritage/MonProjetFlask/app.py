from flask import Flask, render_template, request
from models.etudiant import Etudiant

app = Flask(__name__)


@app.route("/")
def inscription():
    return render_template("inscription.html")


@app.route("/inscription", methods=["POST"])
def traiter_inscription():

    nom = request.form["nom"]
    prenom = request.form["prenom"]
    email = request.form["email"]
    mot_de_passe = request.form["mot_de_passe"]
    age = request.form["age"]
    niveau = request.form["niveau"]
    specialite = request.form["specialite"]

# Création d'un objet User
    etudiant1 = Etudiant(nom, prenom, email, mot_de_passe, age, niveau, specialite)

 # Transmission de l'objet au template
    return render_template("resultat.html", E1= etudiant1)

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)

