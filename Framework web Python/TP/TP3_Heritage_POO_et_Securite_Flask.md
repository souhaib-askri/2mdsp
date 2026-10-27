---
jupyter:
  formats: ipynb,md
  text_representation:
    extension: .md
    format_name: markdown
    format_version: '1.3'
    jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# TP 3 : L'Héritage en POO avec Flask & Hachage Sécurisé des Mots de Passe
## Module : Framework Web Python — 2MDS / A.U. 2026-2027
**Enseignant responsable : Nabil KHEMIRI**

---

## 1. Objectifs du TP

L'objectif de ce travail pratique est d'approfondir l'intégration de la **Programmation Orientée Objet (POO)** au sein du micro-framework **Flask** et de maîtriser les impératifs de sécurité web :
1. **Implémentation de l'héritage en Python** : Créer une hiérarchie de classes (`User` $\to$ `Etudiant`) exploitant `super().__init__()` pour la factorisation du code.
2. **Encapsulation stricte** : Protéger les données sensibles via des attributs privés (`__nom`, `__email`, `__mot_de_passe`, `__niveau`, `__specialite`) et exposer des accesseurs (`get_...`) et mutateurs (`set_...`).
3. **Sécurité cryptographique avec Werkzeug** : Éviter le stockage en texte clair des mots de passe en appliquant un hachage unidirectionnel salé (`generate_password_hash` et `check_password_hash`).
4. **Intégration Flask & Moteur Jinja2** : Traiter des requêtes **POST**, instancier un objet métier complet et restituer ses données dans un template structuré.
5. **Simulation & Benchmarking** : Évaluer les performances temporelles et la résistance cryptographique des algorithmes de hachage (`scrypt`, `pbkdf2:sha256`) via des visualisations graphiques.

---

## 2. Installation & Importations

```python
# Installation des dépendances dans l'environnement virtuel si nécessaire
# !pip install flask werkzeug matplotlib seaborn
```

```python
import os
import sys
import time
import secrets
import matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template_string, request

print(f"Python version : {sys.version.split()[0]}")
import flask
print(f"Flask version  : {flask.__version__}")
```

---

## 3. Modélisation Métier (POO) & Hachage Sécurisé

### 3.1 Classe de Base : `User` avec Hachage Automatique

La classe mère `User` encapsule les informations générales et hache immédiatement le mot de passe dès l'instanciation.

```python
class User:
    """
    Classe de base représentant un utilisateur générique du système.
    Intègre une sécurité native par hachage cryptographique du mot de passe.
    """
    def __init__(self, nom: str, prenom: str, email: str, mot_de_passe: str, age: int):
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        # Hachage sécurisé : le mot de passe en clair n'est jamais conservé
        self.__mot_de_passe = generate_password_hash(mot_de_passe)
        self.__age = int(age)

    # Getters (Accesseurs)
    def get_nom(self) -> str:
        return self.__nom

    def get_prenom(self) -> str:
        return self.__prenom

    def get_email(self) -> str:
        return self.__email

    def get_age(self) -> int:
        return self.__age

    def get_mot_de_passe(self) -> str:
        return self.__mot_de_passe

    # Setters (Mutateurs)
    def set_nom(self, nom: str):
        self.__nom = nom

    def set_prenom(self, prenom: str):
        self.__prenom = prenom

    def set_email(self, email: str):
        self.__email = email

    def set_age(self, age: int):
        self.__age = int(age)

    # Méthode de vérification sécurisée
    def verifier_mot_de_passe(self, mot_de_passe: str) -> bool:
        """
        Vérifie si le mot de passe fourni correspond au condensat haché.
        Utilise une comparaison à temps constant pour prévenir les timing attacks.
        """
        return check_password_hash(self.__mot_de_passe, mot_de_passe)

    def __repr__(self) -> str:
        return f"<User nom='{self.__nom}' email='{self.__email}'>"
```

### 3.2 Classe Dérivée : `Etudiant` par Héritage

La classe `Etudiant` hérite de `User` via la syntaxe `class Etudiant(User)` et étend le modèle avec les attributs académiques `niveau` et `specialite`.

```python
class Etudiant(User):
    """
    Classe représentant un étudiant, spécialisation de la classe User.
    """
    def __init__(self, nom: str, prenom: str, email: str, mot_de_passe: str, age: int,
                 niveau: str, specialite: str):
        # Appel explicite du constructeur de la classe mère
        super().__init__(nom, prenom, email, mot_de_passe, age)

        # Attributs spécifiques à l'étudiant
        self.__niveau = niveau
        self.__specialite = specialite

    def get_niveau(self) -> str:
        return self.__niveau

    def set_niveau(self, niveau: str):
        self.__niveau = niveau

    def get_specialite(self) -> str:
        return self.__specialite

    def set_specialite(self, specialite: str):
        self.__specialite = specialite

    def __repr__(self) -> str:
        return f"<Etudiant nom='{self.get_nom()}' niveau='{self.__niveau}' specialite='{self.__specialite}'>"
```

### 3.3 Validation & Tests Unitaires du Modèle POO

Vérifions le bon fonctionnement de l'héritage, de l'accès aux méthodes parentes et du mécanisme de vérification du mot de passe.

```python
# Instanciation d'un étudiant de test
etudiant_test = Etudiant(
    nom="Askri",
    prenom="Souhaib",
    email="souhaib@example.com",
    mot_de_passe="SecretP@ssw0rd2026",
    age=24,
    niveau="2MDS",
    specialite="Data Science"
)

# Vérifications des accesseurs
assert etudiant_test.get_nom() == "Askri"
assert etudiant_test.get_niveau() == "2MDS"
assert etudiant_test.get_specialite() == "Data Science"

# Vérification que le mot de passe n'est pas en clair
hash_stocke = etudiant_test.get_mot_de_passe()
assert hash_stocke != "SecretP@ssw0rd2026"
assert hash_stocke.startswith("scrypt:") or hash_stocke.startswith("pbkdf2:")

# Vérification du mot de passe
assert etudiant_test.verifier_mot_de_passe("SecretP@ssw0rd2026") is True
assert etudiant_test.verifier_mot_de_passe("MauvaisMotDePasse") is False

print(" Tous les tests unitaires du modèle POO ont réussi avec succès !")
print(f"Format du hash généré : {hash_stocke[:45]}...")
```

---

## 4. Contrôleur Flask & Simulation de l'Application Web

Nous instancions ici un contrôleur Flask complet capable de traiter les requêtes formulaire en exploitant le modèle `Etudiant`.

```python
app = Flask(__name__)
app.config["SECRET_KEY"] = "cle-secrete-tp3-fwp"

# Template Jinja2 simulant 'resultat.html'
RESULTAT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Fiche Étudiant</title></head>
<body>
    <div style="font-family:sans-serif; max-width:600px; margin:20px auto; padding:20px; border:1px solid #ccc; border-radius:8px;">
        <h2 style="color:#1d4ed8;">Données de l'étudiant (Modèle POO)</h2>
        <p><strong>Nom :</strong> {{ E1.get_nom() }}</p>
        <p><strong>Prénom :</strong> {{ E1.get_prenom() }}</p>
        <p><strong>Email :</strong> {{ E1.get_email() }}</p>
        <p><strong>Âge :</strong> {{ E1.get_age() }} ans</p>
        <p><strong>Niveau :</strong> {{ E1.get_niveau() }}</p>
        <p><strong>Spécialité :</strong> {{ E1.get_specialite() }}</p>
        <hr>
        <p><strong>Condensat sécurisé :</strong></p>
        <code style="background:#f1f5f9; padding:4px; display:block; word-break:break-all;">{{ E1.get_mot_de_passe() }}</code>
    </div>
</body>
</html>
"""

@app.route("/inscription", methods=["POST"])
def traiter_inscription():
    data = request.form
    # Instanciation de l'objet Etudiant avec toutes les données requises
    etudiant1 = Etudiant(
        nom=data.get("nom", ""),
        prenom=data.get("prenom", ""),
        email=data.get("email", ""),
        mot_de_passe=data.get("mot_de_passe", ""),
        age=data.get("age", 0),
        niveau=data.get("niveau", ""),
        specialite=data.get("specialite", "")
    )
    return render_template_string(RESULTAT_TEMPLATE, E1=etudiant1)

print(" Contrôleur Flask et routes configurés avec succès.")
```

### 4.1 Test & Simulation de Soumission via le Test Client

```python
client = app.test_client()

# Simulation d'un formulaire de saisie étudiant
form_payload = {
    "nom": "Ben Salah",
    "prenom": "Amira",
    "email": "amira.bensalah@islaib.rnu.tn",
    "mot_de_passe": "MonSuperMotDePasse!2026",
    "age": "23",
    "niveau": "2MDS",
    "specialite": "Big Data & Machine Learning"
}

response = client.post("/inscription", data=form_payload)

print(f"Code HTTP obtenu : {response.status_code}")
assert response.status_code == 200
html_content = response.data.decode("utf-8")
assert "Ben Salah" in html_content
assert "Big Data & Machine Learning" in html_content
assert "MonSuperMotDePasse!2026" not in html_content  # Le mot de passe en clair ne doit pas fuiter

print(" Simulation HTTP réussie : l'objet POO a été transmis et rendu dans le template sans fuite du mot de passe.")
```

---

## 5. Analyse Comparative des Algorithmes de Hachage & Performance

Pour comprendre pourquoi `Werkzeug` utilise `scrypt` par défaut plutôt que des fonctions simples comme MD5 ou SHA256 directes, mesurons le temps de calcul moyen de génération et de vérification.

```python
import hashlib

# Mesure de performance entre hachage rapide (non sécurisé) et hachage robuste avec salt
passwords = [f"PasswordTest_{i}_{secrets.token_hex(4)}" for i in range(50)]

# 1. SHA-256 brut (Inapproprié pour mots de passe - trop rapide)
t0 = time.perf_counter()
for p in passwords:
    _ = hashlib.sha256(p.encode()).hexdigest()
sha256_time = (time.perf_counter() - t0) / len(passwords) * 1000

# 2. Werkzeug generate_password_hash (scrypt ou pbkdf2 - résistant aux attaques)
t0 = time.perf_counter()
hashes = []
for p in passwords:
    hashes.append(generate_password_hash(p))
werkzeug_gen_time = (time.perf_counter() - t0) / len(passwords) * 1000

# 3. Werkzeug check_password_hash (temps de vérification)
t0 = time.perf_counter()
for p, h in zip(passwords, hashes):
    _ = check_password_hash(h, p)
werkzeug_check_time = (time.perf_counter() - t0) / len(passwords) * 1000

print(f"Temps moyen SHA-256 brut          : {sha256_time:.5f} ms")
print(f"Temps moyen Werkzeug (Génération) : {werkzeug_gen_time:.3f} ms")
print(f"Temps moyen Werkzeug (Validation) : {werkzeug_check_time:.3f} ms")
```

```python
# Visualisation graphique de la résistance temporelle
fig, ax = plt.subplots(figsize=(9, 5))
categories = ["SHA-256 Brut\n(Vulnérable Brute-Force)", "Werkzeug scrypt\n(Génération Sécurisée)", "Werkzeug scrypt\n(Validation Sécurisée)"]
times = [sha256_time, werkzeug_gen_time, werkzeug_check_time]
colors = ["#ef4444", "#3b82f6", "#10b981"]

bars = ax.bar(categories, times, color=colors, width=0.5, edgecolor="#0f172a", linewidth=1.2)
ax.set_ylabel("Temps d'exécution (millisecondes - ms)", fontsize=11, fontweight="bold")
ax.set_title("Comparaison de la Résistance Cryptographique : Coût Computationnel", fontsize=13, fontweight="bold", pad=15)
ax.grid(axis="y", linestyle="--", alpha=0.5)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f"{height:.3f} ms",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom", fontweight="bold", fontsize=10)

plt.tight_layout()
plt.show()
```

---

## 6. Conclusion & Bonnes Pratiques

Ce TP a mis en évidence plusieurs principes clés du développement web moderne :
1. **L'Héritage POO** évite la redondance et structure logiquement les entités du domaine (`Etudiant` étend `User`).
2. **L'Encapsulation** empêche l'accès direct aux variables d'état et assure que toute modification transite par des méthodes contrôlées.
3. **Le Hachage Salé Unidirectionnel** garantit qu'en cas de fuite de la base de données, les mots de passe réels demeurent inaccessibles.
4. **La synergie Flask + Jinja2** permet de transmettre des objets métier complexes directement aux vues HTML sans disperser de variables multiples.
