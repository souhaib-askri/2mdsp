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

# TP 1 : L'Évolution des Architectures de Traitement du Langage : Du RNN au Transformer
## Module : Large Language Models (LLM) — 2MDS & 2MIoT (2026-2027)
### Enseignante : Dr. Kaouther Ezzameli — Institut Supérieur des Langues Appliquées et Informatiques de Béja (ISLAIB)

---

### Objectifs du TP :
1. **Comprendre empiriquement la transition architecturale** ayant permis l'émergence des modèles de fondation modernes : du réseau récurrent simple aux blocs Transformer.
2. **Préparer et vectoriser un corpus textuel réel** : Chargement du jeu de données *IMDB Movie Reviews*, limitation du vocabulaire et normalisation des séquences par remplissage (*padding*).
3. **Implémenter et comparer 5 paradigmes d'apprentissage profond pour le NLP** :
   - **Modèle 1 (RNN Simple)** : Récurrence temporelle de base et étude du phénomène de disparition du gradient (*vanishing gradient*).
   - **Modèle 2 (LSTM)** : Contrôle du flux d'information via des portes logiques différentiables (*forget, input, output gates*).
   - **Modèle 3 (CNN 1D)** : Exploitation du parallélisme des convolutions temporelles pour l'extraction de motifs locaux (*n-grams*).
   - **Modèle 4 (Seq2Seq / Encoder-Decoder)** : Compression d'une phrase en un vecteur de contexte fixe et identification du goulot d'étranglement informationnel (*information bottleneck*).
   - **Modèle 5 (Transformer Mini-Block)** : Intégration du mécanisme d'auto-attention (*self-attention*) avec connexions résiduelles et normalisation par couche (*LayerNormalization*).
4. **Implémenter *from scratch* en pur TensorFlow les briques de l'Attention** :
   - Construction d'une couche personnalisée `ScaledDotProductAttention`.
   - Construction d'une couche modulaire `MultiHeadAttention` gérant les projections linéaires, le découpage multi-têtes (*split heads*), et la recombinaison finale.
5. **Valider rigoureusement par des tests unitaires** le comportement matriciel sur des tenseurs synthétiques $\mathbb{R}^{(64, 50, 512)}$ et sur les données réelles du jeu IMDB.

---

## 1. Installation et Importation des Bibliothèques

```python
# Installation des dépendances si nécessaire dans un environnement neuf
# !pip install tensorflow numpy matplotlib seaborn
```

```python
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from tensorflow.keras import layers, Model, Input
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Configuration de la reproductibilité et de l'affichage
np.random.seed(42)
tf.random.set_seed(42)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
%matplotlib inline

print(f"Version de TensorFlow : {tf.__version__}")
print(f"GPU disponible : {tf.config.list_physical_devices('GPU')}")
```

---

## 2. Partie 1 — Préparation du Dataset et Vectorisation

### 2.1 Chargement des données IMDB
Nous limitons le vocabulaire aux **10 000 mots les plus fréquents** et fixons la longueur maximale des séquences à **200 mots**.

```python
VOCAB_SIZE = 10000
MAX_LEN = 200
EMBEDDING_DIM = 64
BATCH_SIZE = 128
EPOCHS = 2

print("Chargement des données IMDB...")
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=VOCAB_SIZE)

print(f"Taille de l'ensemble d'entraînement : {len(x_train)} critiques")
print(f"Taille de l'ensemble de test : {len(x_test)} critiques")
```

### 2.2 Uniformisation par `pad_sequences`

```python
# Troncature et remplissage (padding) post/pre pour fixer la dimension temporelle à MAX_LEN
x_train = pad_sequences(x_train, maxlen=MAX_LEN, padding='post', truncating='post')
x_test = pad_sequences(x_test, maxlen=MAX_LEN, padding='post', truncating='post')

print(f"Forme de x_train après padding : {x_train.shape}")
print(f"Forme de x_test après padding  : {x_test.shape}")
print(f"Exemple d'une séquence vectorisée (10 premiers indices) : {x_train[0][:10]}")
```

### 2.3 Analyse Théorique

> **Question :** Pourquoi ne peut-on pas donner le texte brut ou des phrases de longueurs différentes directement à nos réseaux de neurones ?
>
> **Réponse :**
> 1. **Nature non numérique du texte brut** : Les réseaux de neurones effectuent des opérations d'algèbre linéaire (multiplications matricielles $W \cdot x + b$) qui exigent des représentations tensorielles numériques continues. Le texte brut doit obligatoirement être transformé en identifiants discrets (*tokenization*) puis projeté dans un espace dense continu (*embedding*).
> 2. **Contrainte de dimension matricielle fixe dans le calcul par lots (*Batching*)** : L'entraînement moderne sur GPU repose sur le calcul simultané d'un mini-lot (*batch*) de taille $(B, T, D)$. Si les phrases possédaient des longueurs variables $T_i$, les tenseurs ne seraient pas rectangulaires, ce qui empêcherait les calculs matriciels parallélisés optimisés. Le *padding* standardise $T = 200$ pour l'ensemble du tenseur.

---

## 3. Entraînement et Comparaison des 5 Architectures

Créons un dictionnaire pour consigner les métriques d'évaluation et le temps d'exécution de chaque modèle :

```python
history_records = {}
training_times = {}
```

---

### 3.1 Modèle 1 — RNN Simple (SimpleRNN)

```python
def build_simple_rnn():
    inputs = Input(shape=(MAX_LEN,))
    x = layers.Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM)(inputs)
    x = layers.SimpleRNN(units=32)(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name="Modele_1_SimpleRNN")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model_rnn = build_simple_rnn()
model_rnn.summary()
```

```python
start_time = time.time()
history_rnn = model_rnn.fit(
    x_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    verbose=1
)
time_rnn = (time.time() - start_time) / EPOCHS
training_times["SimpleRNN"] = time_rnn
history_records["SimpleRNN"] = history_rnn.history
```

---

### 3.2 Modèle 2 — LSTM (Long Short-Term Memory)

```python
def build_lstm():
    inputs = Input(shape=(MAX_LEN,))
    x = layers.Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM)(inputs)
    x = layers.LSTM(units=32)(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name="Modele_2_LSTM")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model_lstm = build_lstm()
model_lstm.summary()
```

```python
start_time = time.time()
history_lstm = model_lstm.fit(
    x_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    verbose=1
)
time_lstm = (time.time() - start_time) / EPOCHS
training_times["LSTM"] = time_lstm
history_records["LSTM"] = history_lstm.history
```

> **Analyse Comparative (RNN vs LSTM) :**
> - **Lequel obtient la meilleure précision ?** Le modèle LSTM surpasse très largement le SimpleRNN dès la première époque (précision de validation ~82-86% contre ~50-60% pour le SimpleRNN).
> - **Pourquoi le RNN simple échoue-t-il sur des textes longs (200 mots) ?**
>   Dans un SimpleRNN, le gradient rétropropagé à travers le temps (*BPTT*) est soumis à la multiplication continue par la matrice des poids $W_{hh}^T$ et la dérivée de la fonction $\tanh$. Pour une séquence de 200 pas, la norme du gradient décroît de manière exponentielle ($\to 0$), provoquant la **disparition du gradient (*vanishing gradient*)**. Le réseau "oublie" ainsi les informations du début de texte.
>   Le LSTM résout ce problème grâce à sa **ligne d'état cellulaire additive ($C_t = f_t * C_{t-1} + i_t * \tilde{C}_t$)**, où les portes régulent la conservation de l'information sans atténuation multiplicative brutale.

---

### 3.3 Modèle 3 — CNN 1D (Convolution Temporelle)

```python
def build_cnn1d():
    inputs = Input(shape=(MAX_LEN,))
    x = layers.Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM)(inputs)
    x = layers.Conv1D(filters=32, kernel_size=5, activation='relu')(x)
    x = layers.GlobalMaxPooling1D()(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name="Modele_3_CNN1D")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model_cnn = build_cnn1d()
model_cnn.summary()
```

```python
start_time = time.time()
history_cnn = model_cnn.fit(
    x_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    verbose=1
)
time_cnn = (time.time() - start_time) / EPOCHS
training_times["CNN1D"] = time_cnn
history_records["CNN1D"] = history_cnn.history
```

> **Analyse de Vitesse (CNN 1D vs LSTM) :**
> - Le CNN 1D est **significativement plus rapide** à entraîner par époque que le LSTM (gain typique de $3\times$ à $5\times$).
> - **Explication technique :** Les filtres de convolution 1D s'appliquent simultanément sur toutes les fenêtres glissantes de la séquence grâce aux calculs massivement parallélisés du GPU. À l'inverse, le LSTM est intrinsèquement séquentiel : l'état $h_t$ dépend obligatoirement de $h_{t-1}$, ce qui empêche la vectorisation temporelle complète.

---

### 3.4 Modèle 4 — Encodeur-Décodeur (Seq2Seq sans Attention)

```python
def build_encoder_decoder():
    inputs = Input(shape=(MAX_LEN,))
    x = layers.Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM)(inputs)
    
    # 1. Encodeur : retourne uniquement le dernier état caché
    encoder_out = layers.LSTM(units=32, return_sequences=False)(x)
    
    # 2. RepeatVector : duplique le résumé pour chaque pas temporel
    repeated = layers.RepeatVector(MAX_LEN)(encoder_out)
    
    # 3. Décodeur : reconstruit une séquence à partir du résumé
    decoder_out = layers.LSTM(units=32, return_sequences=True)(repeated)
    
    # 4. Pooling et Classification finale
    pooled = layers.GlobalMaxPooling1D()(decoder_out)
    outputs = layers.Dense(1, activation='sigmoid')(pooled)
    
    model = Model(inputs=inputs, outputs=outputs, name="Modele_4_EncoderDecoder")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model_enc_dec = build_encoder_decoder()
model_enc_dec.summary()
```

```python
start_time = time.time()
history_enc_dec = model_enc_dec.fit(
    x_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    verbose=1
)
time_enc_dec = (time.time() - start_time) / EPOCHS
training_times["EncoderDecoder"] = time_enc_dec
history_records["EncoderDecoder"] = history_enc_dec.history
```

> **Analyse du Flux et Goulot d'Étranglement :**
> - **Limite majeure du vecteur de contexte fixe :** L'encodeur force la compression de l'intégralité d'un document (ici 200 mots) dans un unique vecteur de dimension fixe (32 réels). Au fur et à mesure que la longueur augmente ($T > 200, 500, 1000$), ce vecteur devient un **goulot d'étranglement (*information bottleneck*)** sévère : il est mathématiquement impossible de condenser toute l'entropie et la finesse sémantique d'un long texte dans une dimension fixe sans perte d'information majeure.

---

### 3.5 Modèle 5 — Mini-Bloc Transformer (Auto-Attention via Keras Functional API)

```python
def build_transformer_mini():
    inputs = Input(shape=(MAX_LEN,))
    embedded = layers.Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM)(inputs)
    
    # Auto-Attention : Q = K = V = embedded
    attn_out = layers.MultiHeadAttention(num_heads=2, key_dim=EMBEDDING_DIM)(
        query=embedded,
        key=embedded,
        value=embedded
    )
    
    # Connexion résiduelle + Normalisation de couche
    x = layers.Add()([embedded, attn_out])
    x = layers.LayerNormalization(epsilon=1e-6)(x)
    
    # Réduction spatiale et classification
    x = layers.GlobalAveragePooling1D()(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name="Modele_5_TransformerMini")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model_transformer = build_transformer_mini()
model_transformer.summary()
```

```python
start_time = time.time()
history_transformer = model_transformer.fit(
    x_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    verbose=1
)
time_transformer = (time.time() - start_time) / EPOCHS
training_times["TransformerMini"] = time_transformer
history_records["TransformerMini"] = history_transformer.history
```

> **Analyse Finale des Performances du Transformer :**
> Le Transformer allie la rapidité d'exécution du CNN (traitement 100% parallèle de la séquence sur GPU) avec la capacité du LSTM à appréhender des relations contextuelles complexes, tout en éliminant le goulot d'étranglement grâce aux connexions directes $\mathcal{O}(1)$ entre tous les mots de la séquence.

---

## 4. Visualisation Comparative des 5 Modèles

```python
plt.figure(figsize=(15, 5))

# 1. Précision de validation
plt.subplot(1, 2, 1)
for name, hist in history_records.items():
    plt.plot(range(1, EPOCHS + 1), hist['val_accuracy'], marker='o', label=name)
plt.title("Précision de validation (Val Accuracy) par époque", fontsize=12, fontweight='bold')
plt.xlabel("Époque")
plt.ylabel("Accuracy")
plt.ylim(0.45, 0.92)
plt.legend()

# 2. Temps moyen par époque
plt.subplot(1, 2, 2)
names = list(training_times.keys())
times = list(training_times.values())
bars = plt.bar(names, times, color=['#ef4444', '#8b5cf6', '#0284c7', '#d97706', '#16a34a'])
plt.title("Temps d'entraînement moyen par époque (secondes)", fontsize=12, fontweight='bold')
plt.ylabel("Secondes")
plt.xticks(rotation=25)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f"{yval:.2f}s", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()
```

---

## 5. Partie 2 — Implémentation *from scratch* du Mécanisme d'Attention

Implémentons pas à pas les couches mathématiques fondamentales définies par Vaswani et al. (2017).

$$\text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}} + M\right) V$$

---

### Étape 1 & 2 : Scaled Dot-Product Attention

```python
class ScaledDotProductAttention(layers.Layer):
    """
    Couche d'attention par produit scalaire normalisé.
    Formule : Softmax((Q * K^T) / sqrt(d_k) + Mask) * V
    """
    def __init__(self, **kwargs):
        super(ScaledDotProductAttention, self).__init__(**kwargs)

    def call(self, q, k, v, mask=None):
        # 1. Scores bruts : MatMul entre Q et K transposée
        # Forme de Q : (batch, num_heads, seq_len_q, depth)
        # Forme de K : (batch, num_heads, seq_len_k, depth)
        # transpose_b inverse les deux dernières dimensions de K
        matmul_qk = tf.matmul(q, k, transpose_b=True)

        # 2. Mise à l'échelle par la racine de la profondeur d_k
        d_k = tf.cast(tf.shape(k)[-1], tf.float32)
        scaled_attention_logits = matmul_qk / tf.math.sqrt(d_k)

        # 3. Masquage éventuel (padding mask ou causal mask)
        if mask is not None:
            # On ajoute une valeur très fortement négative (-1e9) là où mask == 1
            scaled_attention_logits += (mask * -1e9)

        # 4. Poids d'attention via Softmax sur la dernière dimension
        attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)

        # 5. Multiplication des poids d'attention par les Valeurs V
        output = tf.matmul(attention_weights, v)

        return output, attention_weights
```

---

### Étape 3 : Multi-Head Attention

```python
class MultiHeadAttention(layers.Layer):
    """
    Couche d'Attention Multi-Têtes modulaire.
    Projette Q, K, V en h sous-espaces de dimension depth = d_model // num_heads,
    applique ScaledDotProductAttention en parallèle, puis recombine les sorties.
    """
    def __init__(self, d_model, num_heads, **kwargs):
        super(MultiHeadAttention, self).__init__(**kwargs)
        self.num_heads = num_heads
        self.d_model = d_model

        assert d_model % num_heads == 0, "d_model doit être un multiple entier de num_heads !"
        self.depth = d_model // num_heads

        # 4 projections linéaires apprenables
        self.wq = layers.Dense(d_model)
        self.wk = layers.Dense(d_model)
        self.wv = layers.Dense(d_model)
        self.dense = layers.Dense(d_model)

        self.attention = ScaledDotProductAttention()

    def split_heads(self, x, batch_size):
        """
        Redimensionne le tenseur de (batch_size, seq_len, d_model)
        vers (batch_size, num_heads, seq_len, depth).
        """
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
        return tf.transpose(x, perm=[0, 2, 1, 3])

    def call(self, v, k, q, mask=None):
        batch_size = tf.shape(q)[0]

        # 1. Projections linéaires et découpage multi-têtes
        q = self.split_heads(self.wq(q), batch_size)  # (batch, heads, seq_q, depth)
        k = self.split_heads(self.wk(k), batch_size)  # (batch, heads, seq_k, depth)
        v = self.split_heads(self.wv(v), batch_size)  # (batch, heads, seq_v, depth)

        # 2. Calcul de l'attention scalaire
        scaled_attention, attention_weights = self.attention(q, k, v, mask=mask)

        # 3. Recombinaison des têtes
        # Transpose de (batch, heads, seq, depth) vers (batch, seq, heads, depth)
        scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])
        
        # Fusion des dimensions : (batch, seq, d_model)
        concat_attention = tf.reshape(scaled_attention, (batch_size, -1, self.d_model))

        # 4. Projection dense finale
        output = self.dense(concat_attention)

        return output, attention_weights
```

---

### Étape 4 : Validation et Tests Unitaires

#### 1. Test unitaire sur tenseurs synthétiques aléatoires

```python
# Validation avec des tenseurs aléatoires uniformes
batch_test = 64
seq_len_test = 50
d_model_test = 512
heads_test = 8

q_dummy = tf.random.uniform((batch_test, seq_len_test, d_model_test))
k_dummy = tf.random.uniform((batch_test, seq_len_test, d_model_test))
v_dummy = tf.random.uniform((batch_test, seq_len_test, d_model_test))

print("--- Test 1 : ScaledDotProductAttention ---")
test_scaled_attn = ScaledDotProductAttention()
# Pour tester directement, on passe une dimension de têtes factice
out_sdp, weights_sdp = test_scaled_attn(q_dummy, k_dummy, v_dummy)
print(f"Forme de la sortie SDP : {out_sdp.shape} (Attendu : ({batch_test}, {seq_len_test}, {d_model_test}))")
print(f"Forme des poids SDP    : {weights_sdp.shape} (Attendu : ({batch_test}, {seq_len_test}, {seq_len_test}))")
assert out_sdp.shape == (batch_test, seq_len_test, d_model_test), "Erreur de forme SDP !"

print("\n--- Test 2 : MultiHeadAttention ---")
mha_custom = MultiHeadAttention(d_model=d_model_test, num_heads=heads_test)
out_mha, weights_mha = mha_custom(v=v_dummy, k=k_dummy, q=q_dummy)
print(f"Forme de la sortie MHA : {out_mha.shape} (Attendu : ({batch_test}, {seq_len_test}, {d_model_test}))")
print(f"Forme des poids MHA    : {weights_mha.shape} (Attendu : ({batch_test}, {heads_test}, {seq_len_test}, {seq_len_test}))")
assert out_mha.shape == (batch_test, seq_len_test, d_model_test), "Erreur de dimension finale MHA !"
print("\n[SUCCÈS] Tous les tests unitaires synthétiques sont validés.")
```

#### 2. Test de validation sur données réelles IMDB (Auto-Attention)

```python
print("--- Test 3 : Auto-Attention sur données réelles IMDB ---")

# Extraction d'un échantillon réel d'entraînement
sample_batch_imdb = x_train[:32]  # batch de 32 phrases de 200 mots
print(f"Dimensions de l'échantillon brut : {sample_batch_imdb.shape}")

# Passage par une couche d'Embedding Keras
embedding_layer = layers.Embedding(input_dim=VOCAB_SIZE, output_dim=64)
embedded_imdb = embedding_layer(sample_batch_imdb)
print(f"Dimensions après Embedding : {embedded_imdb.shape} (32 batch, 200 seq, 64 dim)")

# Instanciation de notre MultiHeadAttention en mode Auto-Attention (Q = K = V)
mha_imdb = MultiHeadAttention(d_model=64, num_heads=4)
out_imdb, weights_imdb = mha_imdb(v=embedded_imdb, k=embedded_imdb, q=embedded_imdb)

print(f"Dimensions du tenseur de sortie MHA : {out_imdb.shape}")
print(f"Dimensions de la matrice d'attention  : {weights_imdb.shape} (32 batch, 4 têtes, 200x200)")

assert out_imdb.shape == (32, 200, 64), "Incohérence sur la forme de sortie réelle !"
print("\n[SUCCÈS] Validation sur données réelles IMDB confirmée.")
```

#### Visualisation d'une matrice d'attention réelle (Heatmap)

Visualisons la matrice d'auto-attention pour la première phrase du lot et la première tête d'attention :

```python
plt.figure(figsize=(7, 6))
# On extrait les 30 premiers mots pour un affichage lisible
attn_map_sample = weights_imdb[0, 0, :30, :30].numpy()

sns.heatmap(attn_map_sample, cmap='viridis', cbar=True)
plt.title("Carte de chaleur d'Auto-Attention (Tête 1, 30 premiers mots)", fontsize=11, fontweight='bold')
plt.xlabel("Mots clés (Keys)")
plt.ylabel("Mots requêtes (Queries)")
plt.show()
```

---

## 6. Conclusion et Perspectives

Ce TP a mis en évidence le saut conceptuel et algorithmique du NLP moderne :
1. **Les limites du RNN Simple** : Son incapacité à conserver le contexte sur 200 mots à cause de la disparition du gradient le rend inopérant pour les tâches complexes.
2. **La robustesse du LSTM** : Les portes d'oubli et de mise à jour restaurent un gradient stable mais conservent un coût de calcul séquentiel non parallélisable.
3. **La vitesse du CNN 1D** : Excellent compromis calculatoire pour les motifs locaux, mais aveugle aux dépendances globales ordonnées.
4. **Le saut du Transformer** : En remplaçant la récurrence par l'**Attention Multi-Têtes**, il concilie parallélisme GPU complet et modélisation directe $\mathcal{O}(1)$ de n'importe quelle paire de mots. Cette brique élémentaire est le fondement de tous les LLMs contemporains (BERT, GPT, LLaMA, DeepSeek).
