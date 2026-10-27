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
    
    return render_template(
        "resultat.html",
        nom=nom,
        prenom=prenom,
        email=email,
        mot_de_passe=mot_de_passe,
        date_naissance=date_naissance
    )


# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)

