---
title: "Correction app POO — Application Web Flask Orientée Objet"
subject: "Framework web Python"
type: TP
tags:
  - 2mdsp
  - fwp
  - flask
  - poo
  - oop
  - jinja2
  - mvc
  - python
date: 2026-10-23
---

# Correction app POO — Application Web Flask avec Modèle Métier Orienté Objet

[🇫🇷 Version Française](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/README.md) | [🇸🇦 النسخة العربية (README_AR.md)](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/README_AR.md)

> **Module** : Framework Web Python  
> **Niveau** : 2ème Année Master Data Science Professionnel (2MDSP)  
> **Contexte** : TP 1 — Version Corrigée & Refactorisation Orientée Objet (POO)  
> **Enseignant** : Nabil KHEMIRI  

---

## 📌 Présentation

`Correction app POO` constitue la **version de référence et corrigée** du premier travail pratique du module **Framework Web Python**. Cette application fait évoluer la structure initiale et procédurale ([`App1`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/App1)) vers une véritable architecture web moderne appliquant les principes de la **Programmation Orientée Objet (POO)** et le découplage de responsabilités de type **Modèle-Vue-Contrôleur (MVC)**.

Dans cette implémentation :
- Les données soumises par l'internaute via le formulaire d'inscription ne sont plus manipulées sous forme de variables éparses.
- Elles sont instanciées sous forme d'un objet métier unique [`User`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/models/user.py#L2-L51), respectant une **encapsulation stricte** (attributs privés préfixés par double tiret bas `__`).
- L'objet complet est injecté dans le contexte du moteur de rendu **Jinja2**, qui appelle directement les accesseurs de l'objet (`get_*()`) pour générer le code HTML final.

---

## 🎯 Objectifs Pédagogiques

1. **Intégration Flask & POO** : Articuler harmonieusement un micro-framework web Python avec des classes métier bien modélisées.
2. **Encapsulation stricte des données** : Protéger l'état interne de l'objet `User` via des attributs privés (`__nom`, `__email`, etc.) et exposer uniquement des accesseurs (`get_*`) et mutateurs (`set_*`) contrôlés.
3. **Structuration modulaire en packages Python** : Organiser le projet avec un dossier `models/` contenant un fichier `__init__.py` pour permettre des importations propres (`from models.user import User`).
4. **Appels de méthodes dans les templates Jinja2** : Tirer parti de la puissance de Jinja2 pour invoquer directement les méthodes d'un objet Python transmis au template (`{{ U1.get_nom() }}`).
5. **Préparation à la gestion des exceptions** : Mettre en place un point d'ancrage pour valider les données et lever des exceptions personnalisées (format de l'email, validité de la date) avant ou pendant l'instanciation de l'objet.

---

## 📂 Structure du Répertoire

```text
TP/Correction app POO/
├── app.py                      # Contrôleur principal Flask et routage HTTP
├── models/                     # Package des modèles métier (Business Logic)
│   ├── __init__.py             # Initialisation du package Python models
│   └── user.py                 # Définition de la classe User (POO encapsulée)
├── templates/                  # Vues Jinja2 rendues par le serveur
│   ├── inscription.html        # Formulaire de saisie utilisateur (GET /)
│   └── resultat.html           # Page de résultat exploitant les méthodes de User
├── static/                     # Ressources statiques publiques
│   └── style.css               # Feuille de style CSS moderne
├── user.py                     # Copie source du modèle à la racine
├── inscription.html            # Copie source d'origine du formulaire
├── resultat.html               # Copie source d'origine du résultat
├── style.css                   # Copie source d'origine du style
└── README.md                   # Ce document explicatif
```

> [!NOTE]
> - Le dossier `models/` est un **package Python** grâce à la présence de `__init__.py`. Cela permet à `app.py` d'exécuter `from models.user import User` de manière standard.
> - Le dossier `templates/` contient les templates HTML interprétés par `render_template()`.
> - Le dossier `static/` contient le fichier CSS référencé dans les templates via la fonction `url_for('static', filename='style.css')`.

---

## 🧠 Modélisation Orientée Objet : La Classe `User`

Le fichier [`models/user.py`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/models/user.py) définit la classe métier `User` selon les règles fondamentales de l'encapsulation :

```python
class User:
    # Constructeur d'initialisation
    def __init__(self, nom, prenom, email, mot_de_passe, date_naissance):
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        self.__mot_de_passe = mot_de_passe
        self.__date_naissance = date_naissance

    # Accesseurs (Getters)
    def get_nom(self): return self.__nom
    def get_prenom(self): return self.__prenom
    def get_email(self): return self.__email
    def get_mot_de_passe(self): return self.__mot_de_passe
    def get_date_naissance(self): return self.__date_naissance

    # Mutateurs (Setters)
    def set_nom(self, nom): self.__nom = nom
    def set_prenom(self, prenom): self.__prenom = prenom
    def set_email(self, email): self.__email = email
    def set_mot_de_passe(self, mot_de_passe): self.__mot_de_passe = mot_de_passe
    def set_date_naissance(self, date_naissance): self.__date_naissance = date_naissance
```

### Avantages de cette modélisation :
- **Masquage de l'implémentation** : L'accès direct aux attributs (`user1.__nom`) est bloqué par le mécanisme de *Name Mangling* de Python (`_User__nom`), interdisant toute modification sauvage hors des méthodes de la classe.
- **Contrôle et validation** : Les mutateurs (`set_*`) permettent d'insérer des contrôles d'intégrité avant d'affecter une nouvelle valeur.
- **Cohérence des données** : Toutes les informations décrivant un même utilisateur sont regroupées dans une seule entité logique.

---

## 🔁 Flux d'Exécution et Routage HTTP

### 1. Affichage du Formulaire : `GET /`
```python
@app.route("/")
def inscription():
    return render_template("inscription.html")
```
- Le client interroge la racine du serveur.
- Flask retourne la vue `templates/inscription.html` contenant les champs nécessaires (`nom`, `prenom`, `email`, `mot_de_passe`, `date_naissance`).

### 2. Traitement et Instanciation : `POST /inscription`
```python
@app.route("/inscription", methods=["POST"])
def traiter_inscription():
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    email = request.form["email"]
    mot_de_passe = request.form["mot_de_passe"]
    date_naissance = request.form["date_naissance"]

    # 1. Instanciation du modèle métier avec les données reçues
    user1 = User(nom, prenom, email, mot_de_passe, date_naissance)

    # 2. Transmission de l'objet unique au moteur de template Jinja2
    return render_template("resultat.html", U1=user1)
```

### 3. Rendu Dynamique Jinja2 dans `templates/resultat.html`
Au lieu de lire de simples variables scalaires, Jinja2 interroge l'objet `U1` via ses accesseurs publics :
```html
<div class="container">
    <h2>Informations de l'utilisateur</h2>
    <p><strong>Bonjour :</strong> {{ U1.get_nom() }} {{ U1.get_prenom() }}</p>
    <p><strong>E-mail :</strong> {{ U1.get_email() }}</p>
    <p><strong>Mot de passe :</strong> {{ U1.get_mot_de_passe() }}</p>
    <p><strong>Date de naissance :</strong> {{ U1.get_date_naissance() }}</p>
    <a href="/">Retour au formulaire</a>
</div>
```

---

## ⚖️ Tableau Comparatif : `App1` (Procédural) vs `Correction app POO` (Orienté Objet)

| Critère de Conception | Version Initiale (`App1`) | Version Corrigée (`Correction app POO`) |
| :--- | :--- | :--- |
| **Paradigme de programmation** | Procédural basique | Orienté Objet (POO) |
| **Représentation des données** | 5 variables disparates | 1 instance structurée de la classe `User` |
| **Encapsulation** | Aucune (données brutes exposées) | Stricte (attributs privés `__` + accesseurs `get_*`) |
| **Signature de `render_template`** | `render_template(..., nom=nom, prenom=prenom, email=email, ...)` | `render_template("resultat.html", U1=user1)` |
| **Syntaxe dans le template** | `{{ nom }}`, `{{ prenom }}` | `{{ U1.get_nom() }}`, `{{ U1.get_prenom() }}` |
| **Modularité du code** | Tout est dans `app.py` | Séparation claire (`models/user.py` + `app.py`) |
| **Évolutivité (Scalabilité)** | Nécessite de retoucher les contrôleurs et signatures | Simple ajout de champ dans `User` sans impacter les signatures |

---

## ⚙️ Guide d'Installation & Exécution

### 1. Prérequis
- Python 3.10 ou supérieur.
- Gestionnaire de paquets `pip`.

### 2. Configuration de l'environnement virtuel

**Sous Linux / macOS :**
```bash
# Accéder au dossier du projet
cd "TP/Correction app POO"

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer Flask
pip install Flask
```

**Sous Windows (PowerShell / CMD) :**
```powershell
cd "TP\Correction app POO"
python -m venv venv
.\venv\Scripts\activate
pip install Flask
```

### 3. Démarrage du serveur web

Exécuter le script du contrôleur :
```bash
python app.py
```

Ou via l'utilitaire CLI Flask :
```bash
flask --app app run --debug
```

Le serveur web local sera accessible sur votre navigateur :
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🛠️ Dépannage & Bonnes Pratiques

### 1. `ModuleNotFoundError: No module named 'models'`
- **Origine** : Le répertoire `models/` est introuvable ou le fichier `__init__.py` est absent.
- **Résolution** : Vérifier que le dossier `models` contient bien un fichier `__init__.py` (même vide) et que l'exécution de la commande `python app.py` se fait bien depuis le répertoire racine du projet `Correction app POO/`.

### 2. `TemplateNotFound: inscription.html`
- **Origine** : Les fichiers HTML ne sont pas situés dans le sous-dossier attendu par Flask.
- **Résolution** : S'assurer que les fichiers `inscription.html` et `resultat.html` sont présents dans le sous-dossier `templates/`.

### 3. `Address already in use` (Port 5000 occupé)
- **Origine** : Une autre instance de serveur Flask ou un service système occupe déjà le port 5000.
- **Résolution** : Modifier le port dans [`app.py`](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO/app.py#L29) :
  ```python
  if __name__ == "__main__":
      app.run(debug=True, port=5001)
  ```
  Puis ouvrir `http://127.0.0.1:5001`.

---

## 🔗 Liens & Références Connexes

- Version d'initiation procédurale : [App1 (README.md)](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/App1/README.md)
- Fiche de synthèse Obsidian (Atelier 1) : [01_Atelier_1_Installation_Flask_et_Application_Web_POO.md](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/01_Atelier_1_Installation_Flask_et_Application_Web_POO.md)
- Cahier de TP interactif Jupytext : [TP1_Installation_Flask_et_Application_Web_POO.ipynb](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/TP1_Installation_Flask_et_Application_Web_POO.ipynb)
- Rappels de cours POO & Architectures Web : [01_Rappels_Architectures_Web_et_POO_Python.md](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/Cours/01_Rappels_Architectures_Web_et_POO_Python.md)
- Gestion des Exceptions en Python : [02_Gestion_des_Exceptions_en_Python.md](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/Cours/02_Gestion_des_Exceptions_en_Python.md)
