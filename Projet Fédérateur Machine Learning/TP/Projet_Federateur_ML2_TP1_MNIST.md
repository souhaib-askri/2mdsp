---
jupyter:
  formats: ipynb,md
  jupytext:
    formats: ipynb,md
    notebook_metadata_filter: formats,text_representation
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.3
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  text_representation:
    extension: .md
    format_name: markdown
    format_version: '1.3'
    jupytext_version: 1.16.4
---

# TP1 : Projet Fédérateur ML2 — Introduction au Deep Learning et Exploration des Données MNIST

**Matière** : Machine Learning 2 / Deep Learning  
**Enseignante** : Mme Manel JERBI  
**Bibliothèques requises** : `NumPy`, `Matplotlib`, `TensorFlow / Keras`

---

## 1. Présentation & Objectifs du Projet Fédérateur

### 1.1. Contexte Général
L'apprentissage automatique (**Machine Learning**) et l'apprentissage profond (**Deep Learning**) occupent une place centrale dans la conception des systèmes d'intelligence artificielle modernes. Ces modèles permettent aux machines d'extraire automatiquement des représentations à partir de données brutes pour accomplir des tâches complexes telles que la vision par ordinateur (**Computer Vision**), la détection d'anomalies et le traitement du langage naturel.

Dans ce projet fédérateur, nous nous attaquons à la problématique de la **reconnaissance automatique de chiffres manuscrits**. Comment un modèle informatique peut-il reconnaître avec fiabilité un chiffre tracé à la main malgré l'extrême variabilité des styles d'écriture ?

### 1.2. Objectifs d'Apprentissage du TP1 :
1. **Prise en main de l'écosystème Deep Learning** : Maîtriser le rôle complémentaire de `NumPy`, `Matplotlib` et `TensorFlow`.
2. **Ingestion du jeu de données de référence MNIST** : Charger et partitionner les sous-ensembles d'apprentissage et de test.
3. **Exploration géométrique & matricielle** : Décortiquer les dimensions tensorielles et la structure interne d'une image matricielle de $28 \times 28$ pixels.
4. **Visualisation & Analyse qualitative** : Inspecter la variabilité inter-classes et intra-classes des tracés manuscrits.
5. **Audit statistique de la distribution des classes** : Évaluer l'équilibre du jeu de données pour prévenir tout biais d'apprentissage.
6. **Résolution complète des exercices d'application** et synthèse théorique.


## 2. Étape 1 — Préparation de l'Environnement et Importations

```python
# Importation des bibliothèques fondamentales
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras.datasets import mnist

# Vérification des versions
print(f"Version de TensorFlow : {tf.__version__}")
print(f"Version de NumPy      : {np.__version__}")
```

### Réponses aux Questions de l'Étape 1 :

> **Question 1 : Quel est le rôle de NumPy ?**  
> **Réponse :** `NumPy` est la bibliothèque fondamentale pour le calcul numérique scientifique en Python. Elle fournit la structure de données `ndarray` (tableaux multidimensionnels optimisés en C) permettant de manipuler efficacement les matrices de pixels, d'effectuer des calculs vectorisés, des filtrages par masques booléens et des opérations statistiques sans lenteur.

> **Question 2 : À quoi sert Matplotlib ?**  
> **Réponse :** `Matplotlib` (et plus spécifiquement son sous-module `pyplot`) est l'outil standard de visualisation 2D en Python. Dans ce projet, il permet de restituer visuellement les matrices numériques de pixels sous forme d'images en niveaux de gris (`plt.imshow`), ainsi que de tracer des histogrammes et graphiques en barres pour analyser les distributions statistiques.

> **Question 3 : Pourquoi utilisons-nous TensorFlow dans ce projet ?**  
> **Réponse :** `TensorFlow` (avec son API haut niveau `Keras`) est le framework de Deep Learning de référence industrielle développé par Google. Il offre des modules préconfigurés pour télécharger les jeux de données standards (`tf.keras.datasets`), gère la différenciation automatique par rétropropagation du gradient, et permet de construire, entraîner et déployer des réseaux de neurones profonds optimisés sur GPU/TPU.


## 3. Étape 2 — Chargement du Jeu de Données MNIST
Nous chargeons les données partitionnées automatiquement via l'utilitaire `mnist.load_data()`.

```python
# Chargement du jeu de données MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

print("Données chargées avec succès.")
```

### Explication détaillée des variables :
- **`x_train`** : Tableau NumPy 3D contenant les **60 000 images d'entraînement**. Chaque image est encodée sous la forme d'une matrice $28 \times 28$ de valeurs de pixels entières non signées (`uint8`) comprises entre 0 et 255.
- **`y_train`** : Vecteur 1D contenant les **60 000 étiquettes cibles (labels)** associées aux images d'entraînement (valeurs discrètes de 0 à 9).
- **`x_test`** : Tableau NumPy 3D contenant les **10 000 images de test**, réservées exclusivement à l'évaluation finale impartiale du modèle.
- **`y_test`** : Vecteur 1D contenant les **10 000 étiquettes réelles** des images de test.


## 4. Étape 3 — Exploration des Dimensions Tensorielles

```python
# Affichage des dimensions des tenseurs de données
print("Dimensions x_train :", x_train.shape)
print("Dimensions y_train :", y_train.shape)

print("Dimensions x_test  :", x_test.shape)
print("Dimensions y_test  :", y_test.shape)
```

### Réponses aux Questions de l'Étape 3 :

> **Question 1 : Combien d'images sont disponibles pour l'entraînement ?**  
> **Réponse :** Il y a **60 000 images** dédiées à la phase d'entraînement (`x_train.shape[0] = 60000`).

> **Question 2 : Combien d'images sont disponibles pour le test ?**  
> **Réponse :** Il y a **10 000 images** strictement réservées pour le test (`x_test.shape[0] = 10000`).

> **Question 3 : Que représente la dimension (60000, 28, 28) ?**  
> **Réponse :** C'est un tenseur d'ordre 3 (3D array) indiquant que le jeu d'entraînement est constitué de **60 000 matrices individuelles**, où chaque matrice comporte **28 lignes** (hauteur en pixels) et **28 colonnes** (largeur en pixels).

> **Question 4 : Pourquoi les étiquettes possèdent-elles une seule dimension ?**  
> **Réponse :** Les étiquettes (`y_train` et `y_test`) représentent une information scalaire unidimensionnelle : chaque image correspond exactement à une seule classe cible (un entier unique entre 0 et 9). Il s'agit donc d'un simple vecteur de taille $(N,)$ sans structure spatiale bidimensionnelle.


## 5. Étape 4 — Visualisation d'une Image Individuelle
Affichage de la première image du jeu de données (`indice = 0`), puis de l'image d'indice 25.

```python
# Affichage de la première image (indice 0)
plt.figure(figsize=(3, 3))
plt.imshow(x_train[0], cmap="gray")
plt.title("Chiffre (Indice 0) : " + str(y_train[0]), fontsize=12, fontweight='bold')
plt.axis("off")
plt.show()
```

```python
# Modification demandée : Affichage de l'image d'indice 25
indice_25 = 25
plt.figure(figsize=(3, 3))
plt.imshow(x_train[indice_25], cmap="gray")
plt.title(f"Chiffre (Indice {indice_25}) : {y_train[indice_25]}", fontsize=12, fontweight='bold')
plt.axis("off")
plt.show()

print(f"L'image d'indice {indice_25} représente le chiffre : {y_train[indice_25]}")
```

## 6. Étape 5 — Visualisation Multi-Images & Variabilité d'Écriture
Nous modifions le programme pour afficher **20 images manuscrites** organisées selon une grille de **4 lignes et 5 colonnes**.

```python
# Affichage de 20 images organisées en 4 lignes x 5 colonnes
plt.figure(figsize=(12, 8))

for i in range(20):
    plt.subplot(4, 5, i + 1)
    plt.imshow(x_train[i], cmap="gray")
    plt.title(f"Chiffre : {y_train[i]}", fontsize=11, fontweight='bold')
    plt.axis("off")

plt.tight_layout()
plt.show()
```

### Réponses aux Questions de l'Étape 5 :

> **Question 1 : Les chiffres possèdent-ils toujours la même forme ?**  
> **Réponse :** Non. On observe une très grande hétérogénéité : certains chiffres sont inclinés (italique), d'autres ont un trait très épais ou très fin, certains chiffres 7 ont une barre horizontale médiane tandis que d'autres ne l'ont pas, et la boucle du chiffre 0 ou 6 varie considérablement d'un scripteur à l'autre.

> **Question 2 : Quelles difficultés un modèle pourrait-il rencontrer pour reconnaître certains chiffres ?**  
> **Réponse :** 
> 1. **Ambiguïté inter-classes (confusion morphologique)** : Un `4` mal fermé peut être confondu avec un `9` ; un `1` incliné peut ressembler à un `7` ; un `3` ouvert peut ressembler à un `8` ou un `5`.
> 2. **Variations d'échelle et d'épaisseur de trait** : Certains tracés sont fragmentés ou bruités.

> **Question 3 : Pourquoi est-il nécessaire d'utiliser plusieurs exemples d'une même classe ?**  
> **Réponse :** Pour que le modèle apprenne des caractéristiques invariantes (patterns généraux) et généralise correctement sans sur-apprendre (*overfitting*). Un seul exemple de chaque chiffre forcerait le modèle à mémoriser un style particulier au lieu de capturer l'essence géométrique du concept.


## 7. Étape 6 — Analyse de la Structure Interne des Pixels
Examinons les valeurs scalaires qui composent une image matricielle.

```python
# Sélection de l'image 0
image_0 = x_train[0]

print("Dimensions de l'image      :", image_0.shape)
print("Type de données (dtype)    :", image_0.dtype)
print("Valeur minimale de pixel   :", image_0.min())
print("Valeur maximale de pixel   :", image_0.max())
print("Nombre total de pixels     :", image_0.size, "(28 x 28)")
```

```python
# Visualisation de la matrice de pixels (extrait central)
print("Extrait de la matrice de pixels (lignes 10 à 18, colonnes 10 à 20) :")
print(image_0[10:19, 10:21])
```

### Synthèse sur la Représentation des Pixels :
- **Définition d'un Pixel (*Picture Element*)** : La plus petite unité constitutive d'une image numérique.
- **Encodage** : En niveaux de gris 8 bits (`uint8`), chaque pixel prend une valeur entière entre **0** (noir absolu, fond de l'image) et **255** (blanc éclatant, tracé du chiffre manuscrit).
- **Nombre total de caractéristiques (Features)** : Chaque image contient $28 \times 28 = 784$ pixels.


## 8. Étape 7 — Analyse de la Distribution des Classes
Vérifions si le jeu de données d'entraînement est équilibré entre les 10 chiffres (de 0 à 9).

```python
# Calcul des effectifs par classe
classes, effectifs = np.unique(y_train, return_counts=True)

print("--- Effectifs par classe dans l'ensemble d'entraînement ---")
for chiffre, nombre in zip(classes, effectifs):
    pourcentage = (nombre / len(y_train)) * 100
    print(f"Chiffre {chiffre} : {nombre} images ({pourcentage:.2f}%)")
```

```python
# Représentation graphique de la distribution
plt.figure(figsize=(9, 5))
colors = ['#2563eb' if n != effectifs.max() and n != effectifs.min() else ('#10b981' if n == effectifs.max() else '#f59e0b') for n in effectifs]
bars = plt.bar(classes, effectifs, color=colors, edgecolor='#1e293b', linewidth=1)

# Annotations au sommet des barres
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 50, f"{int(yval)}", ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.axhline(len(y_train)/10, color='#e11d48', linestyle='--', label=f'Moyenne théorique ({int(len(y_train)/10)})')
plt.xlabel("Chiffre manuscrit (Classe)", fontsize=11, fontweight='bold')
plt.ylabel("Nombre d'images", fontsize=11, fontweight='bold')
plt.title("Distribution des Classes dans le Jeu d'Entraînement MNIST", fontsize=13, fontweight='bold', pad=15)
plt.xticks(range(10))
plt.ylim(0, 7500)
plt.legend()
plt.tight_layout()
plt.show()
```

### Réponses aux Questions de l'Étape 7 :
1. **Chiffre le plus représenté** : Le chiffre **1** avec **6 742 images** (~11.24%).
2. **Chiffre le moins représenté** : Le chiffre **5** avec **5 421 images** (~9.04%).
3. **Comparaison des effectifs** : Chaque classe représente environ 9% à 11% des données. L'écart entre le maximum et le minimum n'est que de 1 321 images.
4. **Importance de la distribution** : Un jeu de données équilibré empêche le modèle de favoriser une classe majoritaire (biais prédictif) et garantit que la précision globale reflète fidèlement la performance sur toutes les catégories.


## 9. Exercices d'Application

### Exercice 1 — Exploration de l'Image d'Indice 50

```python
# Implémentation complète de l'Exercice 1
indice = 50

image_50 = x_train[indice]
etiquette_50 = y_train[indice]

print("--- Caractéristiques de l'image indice 50 ---")
print("Étiquette   :", etiquette_50)
print("Dimensions  :", image_50.shape)
print("Minimum     :", image_50.min())
print("Maximum     :", image_50.max())

# Visualisation
plt.figure(figsize=(3, 3))
plt.imshow(image_50, cmap="gray")
plt.title(f"Image {indice} : Chiffre {etiquette_50}", fontweight='bold')
plt.axis("off")
plt.show()
```

### Exercice 2 — Recherche d'Images Appartenant à la Classe 7

```python
# Implémentation de l'Exercice 2
indices_7 = np.where(y_train == 7)[0]
print(f"Nombre total d'images du chiffre 7 disponibles : {len(indices_7)}")

# Sélection de 5 images distinctes
cinq_indices = indices_7[:5]

plt.figure(figsize=(12, 3))
for i, idx in enumerate(cinq_indices):
    plt.subplot(1, 5, i + 1)
    plt.imshow(x_train[idx], cmap="gray")
    plt.title(f"Indice: {idx} | Chiffre: {y_train[idx]}", fontsize=10, fontweight='bold')
    plt.axis("off")

plt.suptitle("Comparaison de 5 Écritures Manuscrites du Chiffre 7", fontsize=13, fontweight='bold', y=1.05)
plt.tight_layout()
plt.show()
```

> **Question de l'Exercice 2 : Les cinq chiffres présentent-ils exactement la même écriture ? Justifier.**  
> **Réponse :** Non. Bien qu'ils représentent tous le chiffre 7, on observe des disparités d'épaisseur de trait, d'inclinaison angulaire, de courbure de la barre supérieure et d'absence/présence de barre transversale. Cela illustre parfaitement la nécessité d'un réseau de neurones capable d'extraire des invariances spatiales.


### Exercice 3 — Comparaison de Deux Classes (Chiffre 0 vs Chiffre 9)

```python
# Implémentation complète de l'Exercice 3
nb_zero = np.sum(y_train == 0)
nb_neuf = np.sum(y_train == 9)
difference = abs(int(nb_zero) - int(nb_neuf))

print("=" * 45)
print(f"Nombre d'images du chiffre 0 : {nb_zero}")
print(f"Nombre d'images du chiffre 9 : {nb_neuf}")
print(f"Différence absolue           : {difference} images")

if nb_neuf > nb_zero:
    print(f"--> Le chiffre 9 est le plus représenté (+{difference} images).")
elif nb_zero > nb_neuf:
    print(f"--> Le chiffre 0 est le plus représenté (+{difference} images).")
else:
    print("--> Les deux classes possèdent exactement le même effectif.")
print("=" * 45)
```

## 10. Synthèse & Questions de Compréhension Théorique

### 1. Différence entre Machine Learning et Deep Learning ?
- **Machine Learning classique** : Nécessite une étape manuelle d'extraction et d'ingénierie des caractéristiques (**Feature Engineering**). Les algorithmes (SVM, Random Forest) reçoivent des descripteurs prétraités.
- **Deep Learning** : Utilise des réseaux de neurones profonds multicouches capables d'apprendre automatiquement les caractéristiques hiérarchiques (**Feature Learning**) directement à partir des pixels bruts.

### 2. Qu'est-ce que l'apprentissage supervisé ?
C'est un paradigme d'apprentissage dans lequel l'algorithme est entraîné à partir d'un ensemble d'exemples étiquetés $\{(x_i, y_i)\}$. Le modèle ajuste ses paramètres internes (poids et biais) pour minimiser l'erreur entre sa prédiction $\hat{y}$ et la vérité terrain $y$.

### 3. Différence entre classification et régression ?
- **Classification** : La variable cible $y$ est discrète ou catégorielle (ex. identifier un chiffre parmi $\{0, 1, ..., 9\}$).
- **Régression** : La variable cible $y$ est continue (ex. prédire un prix, une température).

### 4. Qu'est-ce qu'un pixel ?
C'est le plus petit élément individuel composant une image matricielle (raster). En niveaux de gris 8 bits, il quantifie l'intensité lumineuse locale par un entier de 0 (noir) à 255 (blanc).

### 5. Comment une image est-elle représentée dans un ordinateur ?
Sous la forme d'un tableau multidimensionnel (tenseur) de nombres :
- En niveaux de gris : une matrice 2D de taille $(\text{Hauteur}, \text{Largeur})$.
- En couleur : un tenseur 3D de taille $(\text{Hauteur}, \text{Largeur}, 3)$ correspondant aux 3 canaux Rouge, Vert, Bleu (RGB).

### 6. Pourquoi faut-il séparer les données d'entraînement et de test ?
Pour évaluer la capacité de **généralisation** du modèle sur des données inédites et s'assurer qu'il n'a pas simplement appris par cœur les exemples d'entraînement (**Sur-apprentissage / Overfitting**).

### 7. Quel est l'intérêt d'analyser la distribution des classes avant l'entraînement ?
Pour détecter un éventuel déséquilibre de classes (**Class Imbalance**). Si une classe était sous-représentée (ex. 1% des données), un modèle naïf pourrait l'ignorer totalement tout en affichant un taux d'exactitude trompeur de 99%.
