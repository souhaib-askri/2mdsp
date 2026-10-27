# App1 — Application Web Flask (Formulaire d'Inscription)

> **Module** : Framework Web Python  
> **Niveau** : 2ème Année Master Data Science Professionnel (2MDSP)  
> **Contexte** : TP 1 — Initiation à Flask & Routage HTTP  
> **Enseignant** : Nabil KHEMIRI  

---

## 📌 Présentation

`App1` est la première application web développée dans le cadre des travaux pratiques du module **Framework Web Python**. Il s'agit d'une application d'initiation construite avec le micro-framework **Flask**, permettant aux utilisateurs de saisir leurs informations d'inscription via un formulaire web, de soumettre les données au serveur en `POST`, et de visualiser un récapitulatif formaté.

Cette version illustre l'approche **procédurale** du traitement des requêtes avant sa transition vers le paradigme **Orienté Objet (POO)** implémenté dans `Correction app POO`.

---

## 🎯 Objectifs Pédagogiques

1. **Initialisation d'un serveur Flask** : Comprendre le rôle de l'instance `Flask(__name__)` et le bloc d'exécution `app.run(debug=True)`.
2. **Gestion des méthodes HTTP** :
   - Requête **GET** pour distribuer la page HTML contenant le formulaire.
   - Requête **POST** pour récupérer et traiter les données soumises par l'internaute.
3. **Extraction des données de formulaire** : Utiliser l'objet contextuel `request.form` pour extraire les paramètres.
4. **Moteur de Templates Jinja2** : Rendre des pages dynamiques avec `render_template()` en transmettant des variables Python au template HTML.
5. **Organisation des assets** : Respecter les conventions de nommage et d'arborescence imposées par Flask (`templates/` et `static/`).

---

## 📂 Structure du Répertoire

```text
TP/App1/
├── app.py                  # Script principal : contrôleur et routes Flask
├── templates/              # Dossier obligatoire pour les vues Jinja2
│   ├── inscription.html    # Formulaire de saisie (vue GET /)
│   └── resultat.html       # Page d'affichage du résultat (vue POST /inscription)
├── static/                 # Dossier obligatoire pour les fichiers statiques
│   └── style.css           # Feuille de style CSS pour l'habillage des pages
├── inscription.html        # Fichier source d'origine
├── resultat.html           # Fichier source d'origine
├── style.css               # Fichier source d'origine
└── README.md               # Ce document
```

> [!NOTE]
> Flask exige par défaut que les fichiers `.html` rendus par `render_template()` soient placés dans le sous-dossier `templates/`, et que les fichiers statiques (`.css`, `.js`, images) soient dans `static/`. Les fichiers `.html` et `.css` présents à la racine de `App1/` proviennent de l'archive initiale (`App1.zip`) et ont été organisés dans leurs dossiers respectifs pour permettre le fonctionnement normal du serveur.

---

## ⚙️ Prérequis & Installation

### 1. Prérequis
- Python 3.10 ou supérieur installé sur la machine.
- Gestionnaire de paquets `pip`.

### 2. Création et activation de l'environnement virtuel

Il est recommandé d'exécuter l'application dans un environnement virtuel dédié :

**Sur Linux / macOS :**
```bash
# Se positionner dans le dossier App1
cd "TP/App1"

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate
```

**Sur Windows (PowerShell / CMD) :**
```powershell
cd "TP\App1"
python -m venv venv
.\venv\Scripts\activate
```

### 3. Installation des dépendances

Installer le framework Flask :
```bash
pip install Flask
```

---

## 🚀 Démarrage de l'Application

Lancez le script principal :
```bash
python app.py
```

Ou via la CLI Flask :
```bash
flask --app app run --debug
```

Le serveur local démarre alors sur le port par défaut :
👉 Ouvrez votre navigateur à l'adresse : **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🛣️ Description des Routes & Fonctionnement

### 1. Route racine `/` (`GET`)
- **Fonction associée** : `inscription()`
- **Comportement** : Retourne la page `templates/inscription.html`.
- **Champs du formulaire** :
  - `nom` (Texte, obligatoire)
  - `prenom` (Texte, obligatoire)
  - `email` (Email, obligatoire)
  - `mot_de_passe` (Password, obligatoire)
  - `date_naissance` (Date, obligatoire)

### 2. Route de traitement `/inscription` (`POST`)
- **Fonction associée** : `traiter_inscription()`
- **Comportement** :
  1. Réceptionne la charge utile via `request.form`.
  2. Extrait chaque variable individuellement :
     ```python
     nom = request.form["nom"]
     prenom = request.form["prenom"]
     email = request.form["email"]
     mot_de_passe = request.form["mot_de_passe"]
     date_naissance = request.form["date_naissance"]
     ```
  3. Transmet ces variables au template de confirmation `templates/resultat.html` :
     ```python
     return render_template(
         "resultat.html",
         nom=nom,
         prenom=prenom,
         email=email,
         mot_de_passe=mot_de_passe,
         date_naissance=date_naissance
     )
     ```
  4. Le template Jinja2 injecte ces valeurs dans le DOM :
     ```html
     <p><strong>Bonjour :</strong> {{ nom }} {{ prenom }}</p>
     <p><strong>E-mail :</strong> {{ email }}</p>
     ...
     ```

---

## 🔄 Comparatif : `App1` (Procédural) vs `Correction app POO` (Orienté Objet)

| Critère | Version `App1` (Cette application) | Version `Correction app POO` |
| :--- | :--- | :--- |
| **Paradigme** | Procédural basique | Orienté Objet (POO) |
| **Gestion des données** | Variables indépendantes et non encapsulées | Regroupées dans un modèle `User` (`models/user.py`) |
| **Encapsulation** | Aucune (valeurs brutes) | Attributs privés (`__nom`, `__email`, etc.) avec accesseurs `get_*()` |
| **Transmission Jinja2** | 5 paramètres passés à `render_template` | Un seul objet passé : `render_template("resultat.html", U1=user1)` |
| **Affichage Jinja2** | `{{ nom }}`, `{{ email }}` | `{{ U1.get_nom() }}`, `{{ U1.get_email() }}` |
| **Validation métier** | Validation HTML5 basique | Exceptions personnalisées Python (`AgeInvalideException`, etc.) |

---

## 🛠️ Dépannage & Erreurs Fréquentes

### 1. `ModuleNotFoundError: No module named 'models'`
- **Cause** : La ligne 2 de `app.py` contient l'import anticipé `from models.user import User`. Dans `App1`, le package `models/` n'est pas encore créé (il fait l'objet de l'étape suivante du TP).
- **Solution** :
  - Soit commenter la ligne 2 (`# from models.user import User`) si vous souhaitez exécuter `App1` en mode 100% procédural.
  - Soit créer le dossier `models/` avec un fichier `__init__.py` et `user.py` (ou copier depuis `../Correction app POO/models/`).

### 2. `jinja2.exceptions.TemplateNotFound: inscription.html`
- **Cause** : Flask ne trouve pas les templates s'ils sont uniquement à la racine du projet.
- **Solution** : Vérifier que `inscription.html` et `resultat.html` sont bien dans le dossier `templates/`.

### 3. `OSError: [Errno 98] Address already in use` (Port 5000 occupé)
- **Cause** : Un autre serveur ou service (ex. AirPlay, autre instance Flask) utilise le port 5000.
- **Solution** : Spécifier un autre port dans `app.py` :
  ```python
  app.run(debug=True, port=5001)
  ```
  Puis accéder à `http://127.0.0.1:5001`.

---

## 📚 Références & Liens Utiles

- Carnet de TP interactif : [TP1_Installation_Flask_et_Application_Web_POO.ipynb](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/TP1_Installation_Flask_et_Application_Web_POO.ipynb)
- Documentation du cours (Obsidian) : [01_Atelier_1_Installation_Flask_et_Application_Web_POO.md](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/01_Atelier_1_Installation_Flask_et_Application_Web_POO.md)
- Version corrigée Orientée Objet : [Correction app POO](file:///home/askri/Sfac/2mdsp/Framework%20web%20Python/TP/Correction%20app%20POO)
- Documentation officielle de Flask : [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
