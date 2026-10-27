# Importation de la classe Flask pour créer l'application web
# render_template permet d'afficher des pages HTML
# redirect permet de rediriger l'utilisateur vers une autre route
# request permet de récupérer les données envoyées par le navigateur
# session permet de stocker et de récupérer des données de session

from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import uuid
import secrets

app = Flask(__name__)

# Configuration de Flask-Session
app.config["SECRET_KEY"] = secrets.token_hex() #Génère une clé aléatoire sécurisée.
app.config["SESSION_PERMANENT"] = False   #Désactive la durée de vie permanente de la session.
app.config["SESSION_TYPE"] = "filesystem" #Stocke les données de session dans des fichiers sur le serveur.

Session(app) #Active l'extension Flask-Session.

# Associe la fonction index() à l'URL racine "/"
@app.route("/")
def index():

    # Vérifier si l'utilisateur est connecté
    if not session.get("name"):
        return redirect("/login")

     # Si l'utilisateur est connecté, afficher la page index.html
    # en transmettant les informations nécessaires au template
    return render_template(
        "index.html",
        name=session["name"],
        session_id=session["session_id"]
    )

# Autoriser les requêtes GET (affichage du formulaire)
# et POST (envoi des données du formulaire)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Récupérer le nom depuis le formulaire
        session["name"] = request.form.get("name")

        # Créer un identifiant unique une seule fois
        if "session_id" not in session:
            session["session_id"] = str(uuid.uuid4())
        
         # Rediriger l'utilisateur vers la page d'accueil "/"
        return redirect("/")
    # Si la requête est GET, afficher le formulaire de connexion
    return render_template("login.html")

# Associer la fonction logout() à l'URL "/logout"
@app.route("/logout")
def logout():

    # Supprimer toutes les données enregistrées dans la session
    # Cela supprime notamment le nom de l'utilisateur et son identifiant de session
    session.clear()
    # Rediriger l'utilisateur vers la page de connexion "/login"
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
