from flask import Flask, render_template, request
from models.user import User

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
    date_naissance = request.form["date_naissance"]

# Création d'un objet User
    user1 = User(nom, prenom, email, mot_de_passe, date_naissance)

 # Transmission de l'objet au template
    return render_template("resultat.html", U1=user1)

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)

