---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.3
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# TP 1 : Neurone Linéaire et Descente de Gradient
## Machine Learning 2 — Deep Learning

---

### Objectifs du TP :
1. **Comprendre et implémenter l'unité fondamentale de l'apprentissage profond** : le neurone linéaire à une entrée et une sortie.
2. **Assimiler les rôles respectifs du poids synaptique ($w$) et du biais ($b$)** dans la modélisation géométrique de la droite de régression.
3. **Formaliser la boucle d'apprentissage supervisé** :
   $$\text{Données} \longrightarrow \text{Prédiction } (\hat{y}) \longrightarrow \text{Erreur } (e) \longrightarrow \text{Fonction de perte } (\text{MSE}) \longrightarrow \text{Gradients } (\nabla) \longrightarrow \text{Mise à jour}$$
4. **Implémenter manuellement en pur NumPy l'algorithme de descente de gradient** sans recourir à des bibliothèques de haut niveau pour l'optimisation.
5. **Analyser l'impact critique du taux d'apprentissage (*learning rate* $\eta$)** sur la vitesse de convergence, la stabilité et le risque de divergence.
6. **Démontrer l'importance de la standardisation des données (*Z-score*)** pour le conditionnement de la surface de perte.
7. **Évaluer les capacités de généralisation** sur des sous-ensembles d'entraînement et de validation, et comparer la solution approchée avec la **solution analytique exacte des Moindres Carrés Ordinaires (MCO)**.

---

## 1. Installation et Importation des Bibliothèques

```python
# Installation des dépendances si nécessaire
# !pip install numpy pandas matplotlib scikit-learn
```

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Configuration de l'affichage graphique
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
%matplotlib inline
```

---

## 2. Partie 1 — Génération et Chargement du Dataset

Nous simulons un problème de régression univariée inspiré du jeu de données classique *California Housing*. La variable d'entrée représente le nombre moyen de pièces par logement (`AveRooms`), et la cible à prédire est la valeur médiane du logement (`PRICE`).

$$y = 0.8 \cdot x + 1.5 + \epsilon, \quad \epsilon \sim \mathcal{N}(0, 0.5^2)$$

```python
# Fixation de la graine pseudo-aléatoire pour la reproductibilité
rng = np.random.default_rng(42)

n = 100
AveRooms = rng.uniform(3.0, 9.0, size=n)
PRICE = (
    0.8 * AveRooms 
    + rng.normal(0.0, 0.5, size=n) 
    + 1.5
)

df = pd.DataFrame({
    'AveRooms': AveRooms,
    'PRICE': PRICE
})

# 1. Affichage des 5 premières lignes
print("--- 5 premières lignes du dataset ---")
print(df.head())

# 2. Dimensions du dataset
print(f"\nTaille du dataset : {df.shape[0]} observations, {df.shape[1]} variables.")

# 3 & 4. Identification des variables
print("\nVariable d'entrée (Feature X) : 'AveRooms' (Nombre moyen de pièces)")
print("Variable cible à prédire (Target y) : 'PRICE' (Prix en dizaines de milliers de $)")
```

---

## 3. Partie 2 — Exploration Visuelle des Données (EDA)

Traçons un nuage de points (*Scatter plot*) pour visualiser la corrélation entre les pièces et le prix.

```python
plt.figure(figsize=(8, 5))
plt.scatter(df['AveRooms'], df['PRICE'], color='#2563eb', alpha=0.8, edgecolors='none', s=45, label='Observations')
plt.title("Relation entre le nombre de pièces (AveRooms) et le Prix", fontsize=13, weight='bold')
plt.xlabel("AveRooms (Nombre moyen de pièces)", fontsize=11)
plt.ylabel("PRICE (Prix du logement)", fontsize=11)
plt.legend()
plt.show()
```

---

## 4. Partie 3 — Standardisation des Données (*Z-Score Normalization*)

La standardisation transforme les caractéristiques pour leur conférer une moyenne nulle ($\mu = 0$) et un écart-type unitaire ($\sigma = 1$) :

$$X_n = \frac{X - \mu}{\sigma}$$

```python
# Extraction sous forme de tableaux NumPy
X = df['AveRooms'].values
y = df['PRICE'].values

# Standardisation de X
Xn = (X - X.mean()) / X.std()

print("Avant standardisation :")
print(f"Moyenne : {X.mean():.4f}")
print(f"Écart-type : {X.std():.4f}")

print("\nAprès standardisation :")
print(f"Moyenne : {Xn.mean():.4e} (sensiblement 0)")
print(f"Écart-type : {Xn.std():.4f} (sensiblement 1)")
```

> **Réponses aux questions :**
> 1. La moyenne de $X_n$ est égale à $0.0000$ (aux erreurs d'arrondi machine près).
> 2. L'écart-type de $X_n$ vaut exactement $1.0000$.
> 3. C'est parfaitement cohérent avec la définition de la loi normale centrée réduite : en soustrayant l'espérance, on centre la distribution sur zéro, et en divisant par l'écart-type, on normalise sa dispersion.

---

## 5. Partie 4 & 5 — Premier Modèle : Neurone Linéaire Sans Biais

Dans cette première étape, nous contraignons le modèle à passer par l'origine :

$$\hat{y} = w \cdot x$$

### Formules fondamentales :
- **Erreur individuelle** : $e = \hat{y} - y$
- **Fonction de perte (MSE)** : $\mathcal{L}(w) = \frac{1}{n} \sum_{i=1}^n (\hat{y}_i - y_i)^2$
- **Gradient analytique** : $\frac{\partial \mathcal{L}}{\partial w} = \frac{2}{n} \sum_{i=1}^n e_i \cdot x_i = 2 \cdot \text{moyenne}(e \cdot x)$
- **Mise à jour** : $w \leftarrow w - \eta \cdot \frac{\partial \mathcal{L}}{\partial w}$

```python
def train_linear_no_bias(X, y, lr=0.05, epochs=200):
    w = 0.0
    losses = []
    
    for epoch in range(epochs):
        # 1. Prédiction
        yhat = w * X
        
        # 2. Erreur
        error = yhat - y
        
        # 3. Fonction de perte (MSE)
        loss = np.mean(error ** 2)
        losses.append(loss)
        
        # 4. Calcul du gradient
        grad_w = 2 * np.mean(error * X)
        
        # 5. Règle de mise à jour de descente de gradient
        w = w - lr * grad_w
        
    return w, np.array(losses)

# Entraînement du modèle sans biais
w1, losses1 = train_linear_no_bias(Xn, y, lr=0.05, epochs=200)

print(f"Poids appris w1 (sans biais) : {w1:.4f}")
print(f"Perte finale MSE : {losses1[-1]:.4f}")

# Visualisation de la courbe d'apprentissage
plt.figure(figsize=(8, 4))
plt.plot(losses1, color='#dc2626', linewidth=2)
plt.xlabel("Epoch", fontsize=11)
plt.ylabel("MSE (Mean Squared Error)", fontsize=11)
plt.title("Évolution de la perte — Modèle sans biais (ŷ = wx)", fontsize=13, weight='bold')
plt.show()
```

> **Observation :**
> La perte diminue rapidement au cours des 20 premières époques avant de se stabiliser sur un plateau. Cependant, le modèle sans biais reste bloqué avec une erreur résiduelle élevée ($\text{MSE} \approx 40$), car il est incapable de translater la droite verticalement.

---

## 6. Partie 6 — Modèle Complet : Neurone Linéaire Avec Biais

Nous ajoutons maintenant le paramètre de biais $b$ :

$$\hat{y} = w \cdot x + b$$

### Gradients analytiques :
$$\frac{\partial \mathcal{L}}{\partial w} = 2 \cdot \text{moyenne}(e \cdot x), \qquad \frac{\partial \mathcal{L}}{\partial b} = 2 \cdot \text{moyenne}(e)$$

```python
def train_linear_with_bias(X, y, lr=0.05, epochs=250):
    w = 0.0
    b = 0.0
    losses = []
    
    for epoch in range(epochs):
        # 1. Prédiction
        yhat = w * X + b
        
        # 2. Erreur
        error = yhat - y
        
        # 3. Fonction de perte MSE
        loss = np.mean(error ** 2)
        losses.append(loss)
        
        # 4. Gradients partiels
        grad_w = 2 * np.mean(error * X)
        grad_b = 2 * np.mean(error)
        
        # 5. Mise à jour simultanée des paramètres
        w = w - lr * grad_w
        b = b - lr * grad_b
        
    return w, b, np.array(losses)

# Entraînement du modèle complet
w2, b2, losses2 = train_linear_with_bias(Xn, y, lr=0.05, epochs=250)

print(f"Poids appris w2 : {w2:.4f}")
print(f"Biais appris b2 : {b2:.4f}")
print(f"Perte finale MSE avec biais : {losses2[-1]:.4f}")
```

---

## 7. Partie 7 — Comparaison des Modèles et Visualisation de la Droite Apprise

Traçons la droite de prédiction obtenue sur le nuage de points des données standardisées.

```python
plt.figure(figsize=(9, 5))

# Données réelles
plt.scatter(Xn, y, color='#2563eb', alpha=0.7, s=40, label='Données réelles')

# Droite du modèle sans biais
plt.plot(Xn, w1 * Xn, color='#dc2626', linestyle='--', linewidth=2, label=f'Sans biais : ŷ = {w1:.2f}x (MSE={losses1[-1]:.2f})')

# Droite du modèle avec biais
plt.plot(Xn, w2 * Xn + b2, color='#16a34a', linewidth=2.5, label=f'Avec biais : ŷ = {w2:.2f}x + {b2:.2f} (MSE={losses2[-1]:.2f})')

plt.title("Ajustement des modèles linéaires sur les données standardisées", fontsize=13, weight='bold')
plt.xlabel("Xn (AveRooms standardisé)", fontsize=11)
plt.ylabel("PRICE", fontsize=11)
plt.legend(fontsize=10)
plt.show()
```

> **Réponses aux questions :**
> 1. **La droite suit-elle la tendance générale des données ?**
>    Oui, le modèle avec biais (en vert) capture parfaitement la pente positive reliant le nombre de pièces au prix moyen.
> 2. **Pourquoi tous les points ne sont-ils pas sur la droite ?**
>    Parce que les données réelles comportent un bruit statistique stochastique ($\epsilon \sim \mathcal{N}(0, 0.5^2)$). Une relation déterministe pure n'existe pas en pratique dans les phénomènes réels.
> 3. **Que représente la distance entre un point et la droite ?**
>    Elle représente le **résidu** ou l'**erreur individuelle** ($e_i = \hat{y}_i - y_i$). C'est cette distance (élevée au carré) que la fonction de perte cherche globalement à minimiser.

---

## 8. Partie 8 — Séparation Entraînement / Validation et Évaluation (MSE & MAE)

Pour mesurer l'aptitude du modèle à généraliser sur des données inconnues, nous subdivisons le jeu en $80\%$ d'entraînement et $20\%$ de validation.

```python
# Séparation 80% train / 20% validation
Xtr, Xva, ytr, yva = train_test_split(Xn, y, test_size=0.20, random_state=42)

# Entraînement sur le jeu d'entraînement uniquement
w_tr, b_tr, losses_tr = train_linear_with_bias(Xtr, ytr, lr=0.05, epochs=250)

# Prédictions
y_pred_tr = w_tr * Xtr + b_tr
y_pred_va = w_tr * Xva + b_tr

# Évaluation des métriques
mse_tr = mean_squared_error(ytr, y_pred_tr)
mae_tr = mean_absolute_error(ytr, y_pred_tr)

mse_va = mean_squared_error(yva, y_pred_va)
mae_va = mean_absolute_error(yva, y_pred_va)

metrics_df = pd.DataFrame({
    'Métrique': ['MSE', 'MAE'],
    'Jeu d\'Entraînement (Train)': [f"{mse_tr:.4f}", f"{mae_tr:.4f}"],
    'Jeu de Validation': [f"{mse_va:.4f}", f"{mae_va:.4f}"]
})

print(metrics_df.to_string(index=False))
```

---

## 9. Partie 9 & 10 — Étude de l'Impact du Learning Rate ($\eta$)

Le taux d'apprentissage (*learning rate*) dicte l'amplitude de chaque pas le long du vecteur opposé au gradient. Testons 5 valeurs : `[0.0005, 0.005, 0.05, 0.2, 0.5]`.

```python
learning_rates = [0.0005, 0.005, 0.05, 0.2, 0.5]

plt.figure(figsize=(12, 6))

lr_results = []

for lr in learning_rates:
    w_tmp, b_tmp, losses_tmp = train_linear_with_bias(Xn, y, lr=lr, epochs=250)
    plt.plot(losses_tmp, label=f"lr = {lr}", linewidth=1.8)
    
    # Analyse de la convergence
    status = "Converge lentement" if lr < 0.01 else ("Converge rapidement et stable" if lr <= 0.2 else "Oscillations / instabilité")
    lr_results.append({
        'Learning Rate': lr,
        'Perte Finale (MSE)': f"{losses_tmp[-1]:.4f}",
        'Comportement': status
    })

plt.title("Convergence de la Descente de Gradient selon le Learning Rate", fontsize=14, weight='bold')
plt.xlabel("Epoch", fontsize=11)
plt.ylabel("MSE", fontsize=11)
plt.ylim(0, 10)
plt.legend(fontsize=11)
plt.show()

# Tableau de synthèse
print(pd.DataFrame(lr_results).to_string(index=False))
```

> **Explication du rôle du Learning Rate :**
> - **$\eta$ trop petit ($0.0005$)** : Le pas de descente est infime. Le modèle requiert des milliers d'époques pour atteindre le minimum, avec un coût de calcul prohibitif.
> - **$\eta$ idéal ($0.05 - 0.2$)** : La descente progresse de manière fluide et atteint le fond de la vallée en une cinquantaine d'époques.
> - **$\eta$ trop grand ($> 0.5$)** : Le pas dépasse le creux de la fonction de perte, provoquant de fortes oscillations voire une divergence vers l'infini (débordement numérique `NaN`).

---

## 10. Partie 11 — Effet de la Standardisation sur l'Optimisation

Comparons la dynamique d'apprentissage sur données brutes ($X$) contre données standardisées ($X_n$).

```python
# Entraînement sans standardisation (nécessite un très faible learning rate pour ne pas diverger)
w_ns, b_ns, losses_ns = train_linear_with_bias(X, y, lr=0.0001, epochs=400)

# Entraînement avec standardisation (permet un learning rate normal de 0.05)
w_s, b_s, losses_s = train_linear_with_bias(Xn, y, lr=0.05, epochs=400)

plt.figure(figsize=(9, 4.5))
plt.plot(losses_ns, label="Sans standardisation (lr = 0.0001)", color='#dc2626', linestyle='--', linewidth=2)
plt.plot(losses_s, label="Avec standardisation (lr = 0.05)", color='#16a34a', linewidth=2)
plt.title("Comparaison de la convergence : Avec vs Sans Standardisation", fontsize=13, weight='bold')
plt.xlabel("Epoch", fontsize=11)
plt.ylabel("MSE", fontsize=11)
plt.ylim(0, 15)
plt.legend(fontsize=10)
plt.show()
```

> **Analyse géométrique :**
> Sans standardisation, la surface de perte forme une ellipse très étirée et asymétrique. Les gradients oscillent fortement dans la direction la plus raide tout en progressant très lentement dans la direction plate.
> Avec la standardisation ($Z$-score), la surface devient symétrique (circulaire), ce qui permet aux gradients de pointer directement vers le minimum global.

---

## 11. Partie 12 — Descente de Gradient vs Solution Analytique (MCO)

La régression linéaire univariée admet une solution fermée mathématiquement exacte donnée par les **Moindres Carrés Ordinaires (MCO / OLS)** :

$$w^* = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} = \frac{\text{Cov}(X, y)}{\text{Var}(X)}, \qquad b^* = \bar{y} - w^* \cdot \bar{x}$$

```python
x_mean = Xn.mean()
y_mean = y.mean()

w_star = np.sum((Xn - x_mean) * (y - y_mean)) / np.sum((Xn - x_mean) ** 2)
b_star = y_mean - w_star * x_mean

comparison_table = pd.DataFrame({
    'Méthode': ['Descente de Gradient (Numérique)', 'Solution Analytique MCO (Exacte)'],
    'Poids (w)': [f"{w2:.5f}", f"{w_star:.5f}"],
    'Biais (b)': [f"{b2:.5f}", f"{b_star:.5f}"],
    'MSE Finale': [f"{losses2[-1]:.5f}", f"{np.mean((w_star * Xn + b_star - y)**2):.5f}"]
})

print(comparison_table.to_string(index=False))
```

> **Conclusion de la comparaison :**
> Les paramètres trouvés par la descente de gradient coïncident avec la solution analytique jusqu'à la 4ème décimale.
> La descente de gradient constitue donc une méthode d'approximation numérique extrêmement puissante qui a l'avantage colossal de se généraliser aux modèles non-linéaires complexes et aux réseaux de neurones profonds, pour lesquels **aucune solution analytique fermée n'existe**.

---

## 12. Synthèse Générale et Conclusion du TP

Au cours de cet atelier pratique :
1. Nous avons reconstruit de bout en bout la dynamique interne d'un neurone artificiel élémentaire.
2. Nous avons vérifié empiriquement la boucle universelle de l'apprentissage machine :
   $$\text{ENTRÉES} \longrightarrow \text{PRÉDICTION} \longrightarrow \text{LOSS} \longrightarrow \text{GRADIENTS} \longrightarrow \text{MISE À JOUR DES PARAMÈTRES}$$
3. Dans les prochains ateliers, nous étendrons ce mécanisme fondamental à des architectures multi-neurones munies de fonctions d'activation non-linéaires (*Sigmoid, ReLU, Softmax*) formant des **réseaux de neurones profonds (*Multilayer Perceptrons - MLP*)**.
