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

# Atelier 1 - Partie 1 : Prétraitement du Langage Naturel (NLP)
## Analyse de Sentiments sur les Données Twitter avec NLTK

---

### Objectifs de l'Atelier :
1. Explorer et préparer un jeu de données textuelles Twitter pour une tâche de **classification de sentiments** (positif vs négatif).
2. Utiliser la boîte à outils **NLTK (Natural Language Toolkit)** pour manipuler les corpus et construire un pipeline de prétraitement.
3. Conduire une **analyse exploratoire des données (EDA)** et visualiser la répartition des classes à l'aide de **Matplotlib**.
4. Inspecter les particularités des textes bruts de réseaux sociaux (URLs, hashtags, mentions, émoticônes).
5. Poser les fondations méthodologiques pour la modélisation prédictive (Partie 2).

---

## 1. Importation des Bibliothèques Requises

Nous importons :
- `nltk` : La bibliothèque de référence en Python pour le traitement du langage naturel.
- `twitter_samples` : Un corpus fourni par NLTK contenant des tweets étiquetés manuellement.
- `matplotlib.pyplot` : Pour la visualisation graphique des données.
- `random` : Pour sélectionner des échantillons aléatoires de tweets.

```python
# Installation des dépendances si nécessaire (ex: dans Google Colab ou nouvel environnement)
# !pip install nltk matplotlib
```

```python
import nltk
from nltk.corpus import twitter_samples
import matplotlib.pyplot as plt
import random
```


---

## 2. Téléchargement du Jeu de Données `twitter_samples`

NLTK intègre des échantillons de tweets prétéléchargeables. Ce corpus est composé de 10 000 tweets annotés :
- 5 000 tweets avec des sentiments positifs.
- 5 000 tweets avec des sentiments négatifs.

```python
# Téléchargement du corpus Twitter depuis les serveurs NLTK
nltk.download('twitter_samples')
```

---

## 3. Chargement des Données en Mémoire

Nous extrayons les textes sous forme de chaînes de caractères brutes grâce à la méthode `.strings()`.

```python
# Chargement des tweets positifs et négatifs
all_positive_tweets = twitter_samples.strings('positive_tweets.json')
all_negative_tweets = twitter_samples.strings('negative_tweets.json')
```

---

## 4. Analyse Exploratoire et Statistiques de Base

La compréhension des données constitue 80 % du succès d'un projet de Data Science. Vérifions les volumes et les types de structures de données manipulées.

```python
# Affichage du nombre de tweets par classe
print(f"Nombre de tweets positifs : {len(all_positive_tweets)}")
print(f"Nombre de tweets négatifs : {len(all_negative_tweets)}")

# Vérification des types
print(f"\nType de la collection : {type(all_positive_tweets)}")
print(f"Type d'un élément (tweet individuel) : {type(all_positive_tweets[0])}")
```

---

## 5. Visualisation Graphique de la Répartition des Classes

Pour produire un rapport visuellement parlant, nous construisons un diagramme circulaire (*Pie Chart*) avec `matplotlib.pyplot`.

```python
# Déclaration de la figure avec une taille appropriée (5x5 pouces)
fig = plt.figure(figsize=(6, 6))

# Étiquettes des deux classes
labels = ['Positifs', 'Négatifs']

# Tailles relatives respectives
sizes = [len(all_positive_tweets), len(all_negative_tweets)]

# Couleurs personnalisées : Vert pour positif, Rouge pour négatif
colors = ['#10b981', '#ef4444']

# Construction du diagramme circulaire
plt.pie(
    sizes, 
    labels=labels, 
    autopct='%1.1f%%', 
    shadow=True, 
    startangle=90, 
    colors=colors,
    textprops={'fontsize': 12, 'weight': 'bold'}
)

# Garantir un rapport d'aspect égal pour un cercle parfait
plt.axis('equal')

# Titre du graphique
plt.title("Distribution des Classes dans le Dataset Twitter", fontsize=14, weight='bold', pad=20)

# Affichage
plt.show()
```

---

## 6. Inspection des Textes Bruts

Avant d'appliquer tout algorithme d'apprentissage, examinons la structure brute des messages.
Nous utilisons des codes de couleur ANSI dans le terminal pour distinguer :
- **En vert (`\033[92m`)** : Un tweet positif aléatoire.
- **En rouge (`\033[91m`)** : Un tweet négatif aléatoire.

```python
# Sélection d'un indice aléatoire entre 0 et 4999
random_index = random.randint(0, len(all_positive_tweets) - 1)

# Affichage du tweet positif en vert
print('\033[92m' + "--- Tweet Positif Aléatoire ---")
print(all_positive_tweets[random_index])

# Affichage du tweet négatif en rouge
print('\n\033[91m' + "--- Tweet Négatif Aléatoire ---")
print(all_negative_tweets[random_index])

# Réinitialisation de la couleur du terminal
print('\033[0m')
```

---

## 7. Synthèse et Observations sur les Données Brutes

À la lecture des tweets bruts, nous constatons plusieurs particularités propres aux réseaux sociaux :

1. **Émoticônes textuelles** : Exemples : `:)`, `:-)`, `:(` qui sont des indicateurs forts de sentiment.
2. **Liens hypertextes (URLs)** : Des liens raccourcis du type `https://t.co/...` qui n'apportent aucune sémantique émotionnelle et doivent être nettoyés.
3. **Mentions d'utilisateurs** : Chaînes de type `@nom_utilisateur` qui représentent du bruit dans un classifieur de sentiments généraliste.
4. **Hashtags** : Symboles `#` accompagnant des mots-clés qu'il faut débarrasser du croisillon tout en conservant le terme sémantique.
5. **Ponctuation redondante et casse mixte** : Nécessite une étape de normalisation.

---

## 8. Étape Suivante : Pipeline de Prétraitement Complet (Aperçu Partie 2)

Voici la fonction de prétraitement complète combinant :
- Nettoyage par **Regex** (suppression de `RT`, URLs, `#`).
- **Tokenisation adaptée aux tweets** (`TweetTokenizer`).
- Suppression des **mots vides (Stopwords)** et de la ponctuation.
- **Racinisation (Stemming)** avec l'algorithme de Porter.

```python
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer

# Téléchargement des mots vides
nltk.download('stopwords')

def process_tweet(tweet):
    """
    Nettoie, tokenise et racinise un tweet brut.
    
    Arguments:
        tweet (str): Le tweet brut à traiter.
    Retourne:
        tweets_clean (list): Liste des tokens nettoyés et racinisés.
    """
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    
    # 1. Supprimer le texte de style retweet "RT"
    tweet2 = re.sub(r'^RT[\s]+', '', tweet)
    
    # 2. Supprimer les hyperliens (URLs)
    tweet2 = re.sub(r'https?://[^\s\n\r]+', '', tweet2)
    
    # 3. Supprimer le symbole '#' des hashtags
    tweet2 = re.sub(r'#', '', tweet2)
    
    # 4. Tokeniser avec TweetTokenizer
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet2)
    
    # 5. Filtrer les stopwords et la ponctuation, puis raciniser
    tweets_clean = []
    for word in tweet_tokens:
        if (word not in stopwords_english and word not in string.punctuation):
            stem_word = stemmer.stem(word)
            tweets_clean.append(stem_word)
            
    return tweets_clean

# Démonstration sur le tweet positif sélectionné
print("--- Démonstration du Pipeline de Prétraitement ---")
print("Tweet original :")
print(all_positive_tweets[random_index])
print("\nTokens après prétraitement complet :")
print(process_tweet(all_positive_tweets[random_index]))
```

---

## 9. Conclusion

Dans cette première partie de l'Atelier 1 :
- Nous avons appréhendé les données du corpus Twitter NLTK (10 000 tweets équilibrés).
- Nous avons mis en place une routine d'observation visuelle et d'analyse exploratoire.
- Nous avons validé la chaîne de prétraitement nécessaire pour convertir les données textuelles non structurées en vecteurs de caractéristiques exploitables par un modèle de Machine Learning (régression logistique ou Naive Bayes dans la Partie 2).
