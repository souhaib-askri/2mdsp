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

# TD 1 : Initiation aux Réseaux de Neurones - Perceptron Simple sur MNIST
**Module** : Large Language Models (LLM)  
**Enseignant** : Dr. K. EZZAMELI  
**Niveau** : Master 2 Data Science (2MDSP)  

---

## 1. Objectifs de la séance

1. Charger et explorer la base de données de référence **MNIST** depuis `tensorflow.keras.datasets`.
2. Visualiser les échantillons sous forme matricielle avec `matplotlib.pyplot.matshow`.
3. Prétraiter et normaliser les données dans l'intervalle $[0, 1]$.
4. Aplatir (Flattening / Reshape) les images de dimensions $(28 \times 28)$ en vecteurs $1D$ de taille $784$.
5. Concevoir une architecture de **Perceptron Simple** (Dense Layer à 10 neurones avec activation Sigmoïde) sans couche cachée.
6. Compiler et entraîner le modèle avec l'optimiseur Adam et la fonction de perte `sparse_categorical_crossentropy`.
7. Évaluer la performance et analyser les prédictions sur l'ensemble de test.

---

## 2. Installation et Importations

```python
# Installation optionnelle si exécuté dans un environnement vierge
# !pip install tensorflow matplotlib numpy seaborn
```

```python
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

print(f"TensorFlow version : {tf.__version__}")
```

---

## 3. Question 1 : Chargement du jeu de données MNIST

> **Énoncé (Question 1)** : Charger le jeu de données mnist à partir de `keras.datasets` de la bibliothèque tensorflow en utilisant `load_data()`. Sauvegarder les données chargées dans `(x_train, y_train)` et `(x_test, y_test)`.

```python
# Chargement du dataset MNIST
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

print(f"Dimensions de x_train : {x_train.shape} (Type : {x_train.dtype})")
print(f"Dimensions de y_train : {y_train.shape}")
print(f"Dimensions de x_test  : {x_test.shape}")
print(f"Dimensions de y_test  : {y_test.shape}")
```

---

## 4. Question 2 : Visualisation d'une image et inspection de ses dimensions

> **Énoncé (Question 2)** : Choisir une image, l'afficher en utilisant `matshow` de `matplotlib.pyplot` et afficher ses dimensions.

```python
# Sélection d'une image d'exemple (index 0)
sample_idx = 0
sample_image = x_train[sample_idx]
sample_label = y_train[sample_idx]

# Affichage avec matshow
plt.matshow(sample_image, cmap='gray')
plt.title(f"Échantillon n°{sample_idx} - Chiffre manuscrit : {sample_label}", pad=15)
plt.colorbar(label="Intensité des pixels (0 à 255)")
plt.show()

# Affichage des dimensions
print(f"Dimensions de l'image sélectionnée : {sample_image.shape}")
print(f"Valeur minimale du pixel : {np.min(sample_image)}")
print(f"Valeur maximale du pixel : {np.max(sample_image)}")
```

---

## 5. Question 3 : Normalisation des données

> **Énoncé (Question 3)** : Normaliser la base de donnée en divisant `x_train` et `x_test` sur 255 pour obtenir dans chaque image des valeurs entre 0 et 1.

```python
# Normalisation min-max par division par 255.0
x_train = x_train / 255.0
x_test = x_test / 255.0

print(f"Nouvelle valeur minimale (x_train) : {np.min(x_train):.1f}")
print(f"Nouvelle valeur maximale (x_train) : {np.max(x_train):.1f}")
```

---

## 6. Question 4 : Redimensionnement (Reshape / Flattening)

> **Énoncé (Question 4)** : Modifier les dimensions de `x_train` et `x_test` pour les adapter au modèle en utilisant la fonction `reshape`. Selon la taille des images :  
> `x_train_flatten = x_train.reshape(len(x_train), 28*28)`  
> `x_test_flatten = x_test.reshape(len(x_test), 28*28)`

```python
# Aplatissement des images 28x28 en vecteurs 784
x_train_flatten = x_train.reshape(len(x_train), 28 * 28)
x_test_flatten = x_test.reshape(len(x_test), 28 * 28)

print(f"Dimensions de x_train_flatten : {x_train_flatten.shape}")
print(f"Dimensions de x_test_flatten  : {x_test_flatten.shape}")
```

---

## 7. Question 5 : Construction de l'architecture du Perceptron Simple

> **Énoncé (Question 5)** : Construire un réseau de neurone avec un perceptron simple en utilisant `sequential` de keras et les paramètres suivants :  
> - Le nombre de classes dans la base est 10 (de 0 à 9).  
> - La taille d'une image entrée est égale à 28*28 (784).  
> - La fonction d'activation est sigmoid.  
>  
> `model = keras.Sequential([keras.layers.Dense(10, input_shape=(784,), activation='sigmoid')])`

```python
# Définition du modèle Perceptron Simple
model = keras.Sequential([
    keras.layers.Dense(10, input_shape=(784,), activation='sigmoid')
])

# Inspection du modèle
model.summary()
```

### Analyse du nombre de paramètres :
$$\text{Total Paramètres} = (\text{Entrées} \times \text{Sorties}) + \text{Biais} = (784 \times 10) + 10 = 7840 + 10 = 7850$$

---

## 8. Question 6 : Compilation et Entraînement du modèle

> **Énoncé (Question 6)** : Compiler le modèle en utilisant `model.compile` avec les paramètres suivants :  
> - Optimiseur : `'adam'`  
> - Fonction de perte : `'sparse_categorical_crossentropy'`  
> - Métrique : `['accuracy']`

```python
# Compilation du modèle
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Entraînement sur 5 époques
history = model.fit(
    x_train_flatten, 
    y_train, 
    epochs=5, 
    batch_size=32,
    validation_split=0.1
)
```

---

## 9. Évaluation et Visualisation des Résultats

```python
# Évaluation sur la base de test
test_loss, test_accuracy = model.evaluate(x_test_flatten, y_test)
print(f"\n--- RÉSULTATS SUR L'ENSEMBLE DE TEST ---")
print(f"Perte (Loss) sur le jeu de test      : {test_loss:.4f}")
print(f"Précision (Accuracy) sur le jeu de test : {test_accuracy * 100:.2f}%")
```

```python
# Tracé des courbes d'apprentissage (Loss & Accuracy)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy
ax1.plot(history.history['accuracy'], label='Entraînement', color='#2563eb', linewidth=2)
ax1.plot(history.history['val_accuracy'], label='Validation', color='#10b981', linewidth=2, linestyle='--')
ax1.set_title("Évolution de la Précision (Accuracy)")
ax1.set_xlabel("Époque")
ax1.set_ylabel("Précision")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Loss
ax2.plot(history.history['loss'], label='Entraînement', color='#dc2626', linewidth=2)
ax2.plot(history.history['val_loss'], label='Validation', color='#f59e0b', linewidth=2, linestyle='--')
ax2.set_title("Évolution de la Perte (Loss)")
ax2.set_xlabel("Époque")
ax2.set_ylabel("Perte")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

```python
# Test de prédiction sur un échantillon individuel
test_sample_idx = 7
test_image = x_test[test_sample_idx]
true_label = y_test[test_sample_idx]

# Prédiction
pred_probs = model.predict(x_test_flatten[test_sample_idx:test_sample_idx+1])
predicted_class = np.argmax(pred_probs[0])

plt.matshow(test_image, cmap='gray')
plt.title(f"Vrai Label : {true_label} | Prédiction : {predicted_class}", pad=15)
plt.show()

print(f"Vecteur de probabilités brutes (10 neurones de sortie) :")
for c, p in enumerate(pred_probs[0]):
    print(f"Classe {c} : {p:.4f}")
```

---

## 10. Conclusion et Synthèse

1. **Simplicité et Efficacité** : Avec seulement une couche dense et 7 850 paramètres, le perceptron simple atteint plus de **92%** de précision sur MNIST en 5 époques.
2. **Limites de l'architecture** :
   - L'aplatissement direct des images détruit la corrélation spatiale locale entre pixels voisins.
   - L'absence de couches cachées empêche d'extraire des représentations abstraites hiérarchiques.
3. **Perspectives vers les LLMs et les Réseaux Profonds** :
   - Ce modèle constitue la brique de base fondamentale des couches linéaires ($W \cdot x + b$) retrouvées dans les réseaux MLP et les modules Feed-Forward des blocs Transformer.
