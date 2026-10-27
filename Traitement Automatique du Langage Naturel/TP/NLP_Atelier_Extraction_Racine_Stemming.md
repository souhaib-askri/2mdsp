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

# Atelier TALN : Extraction de la Racine du Mot (Stemming / Racinisation)

## 1. Objectifs du TP
L'extraction de la racine (**Stemming** ou **Racinisation**) est une étape fondamentale de la normalisation textuelle en Traitement Automatique du Langage Naturel (**TALN**). Elle vise à tronquer les affixes (préfixes et suffixes) pour ramener différentes variantes flexionnelles ou dérivées d'un mot à une même forme canonique ou radicale (*stem*).

### Objectifs d'apprentissage :
1. **Compréhension algorithmique** : Maîtriser le fonctionnement heuristique des algorithmes de racinisation.
2. **Implémentation pratique avec NLTK** : Utiliser `PorterStemmer` et `SnowballStemmer` (Porter2).
3. **Traitement de listes de mots** : Analyser les variations morphologiques sur une liste lexicale (`exemple_mots`).
4. **Traitement et segmentation de phrases** : Intégrer la tokenisation et le racinage sur un corpus phrastique (`exemple`).
5. **Analyse comparative & Visualisation** : Comparer la précision et le comportement des deux algorithmes sur les terminaisons délicates.


## 2. Installation & Importation des Bibliothèques
Nous utilisons la bibliothèque `nltk` (*Natural Language Toolkit*) ainsi que `pandas` et `matplotlib` pour l'analyse des résultats.

```python
# Installation si nécessaire
# !pip install nltk pandas matplotlib seaborn
```

```python
import nltk
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.tokenize import word_tokenize
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Téléchargement du modèle de tokenisation ponctuelle
nltk.download('punkt')
nltk.download('punkt_tab')
```

## 3. Initialisation des Raciniseurs (Stemmers)
Nous instancions le `PorterStemmer` original (développé par Martin Porter en 1980) et le `SnowballStemmer` configuré pour la langue anglaise (`language='english'`, également connu sous le nom d'algorithme Porter2, créé en 2001).

```python
# Instanciation des stemmers
porter = PorterStemmer()
snowball = SnowballStemmer(language='english')

print("Stemmers initialisés avec succès :")
print(f"1. PorterStemmer   : {porter}")
print(f"2. SnowballStemmer : {snowball} (Langue : {snowball.language})")
```

<!-- #region -->
## 4. Exercice 1 : Racinisation sur une Liste de Mots (`exemple_mots`)

Données fournies :
```python
exemple_mots = ["python", "pythoner", "pythoning", "pythoned", "pythonly"]
```

Nous allons extraire le radical de chaque mot avec les deux algorithmes et comparer leurs comportements.
<!-- #endregion -->

```python
# Définition de l'échantillon 1
exemple_mots = ["python", "pythoner", "pythoning", "pythoned", "pythonly"]

# Application du PorterStemmer et SnowballStemmer
resultats_mots = []
for mot in exemple_mots:
    p_stem = porter.stem(mot)
    s_stem = snowball.stem(mot)
    resultats_mots.append({
        "Mot Original": mot,
        "PorterStemmer": p_stem,
        "SnowballStemmer": s_stem,
        "Identiques ?": p_stem == s_stem
    })

df_mots = pd.DataFrame(resultats_mots)
df_mots
```

> [!note] Analyse de l'Exercice 1
> - Pour `pythoning` et `pythoned`, les deux algorithmes éliminent efficacement les suffixes `-ing` et `-ed` pour obtenir la base `python`.
> - Pour `pythoner`, l'algorithme retire le suffixe d'agent `-er`.
> - Pour `pythonly`, le **PorterStemmer** transforme le `y` final en `i` (`pythonli`), tandis que le **SnowballStemmer** applique une règle plus récente et plus robuste qui ramène directement le mot à `python`.

<!-- #region -->
## 5. Exercice 2 : Racinisation d'un Texte Phrastique (`exemple`)

Données fournies :
```python
exemple = "You are not considering the considerable performance considerably. Its consequences will not be considered."
```

### Méthodologie :
1. **Tokenisation** : Découpage du texte en mots et signes de ponctuation via `word_tokenize()`.
2. **Filtrage de la ponctuation** : Conservation des tokens alphanumériques.
3. **Racinisation systématique** : Extraction des radicaux pour chaque token.
<!-- #endregion -->

```python
# Définition de la phrase d'exemple
exemple = "You are not considering the considerable performance considerably. Its consequences will not be considered."

# Étape 1 : Tokenisation
tokens = word_tokenize(exemple)
print(f"Tokens bruts extraits ({len(tokens)}) :")
print(tokens)
```

```python
# Étape 2 : Racinisation comparative sur l'ensemble de la phrase
resultats_phrase = []

for token in tokens:
    # On n'applique le stemmer que sur les mots réels
    if token.isalnum():
        p_stem = porter.stem(token)
        s_stem = snowball.stem(token)
        resultats_phrase.append({
            "Token Original": token,
            "Porter Stem": p_stem,
            "Snowball Stem": s_stem,
            "Égalité": "✓" if p_stem == s_stem else "≠"
        })

df_phrase = pd.DataFrame(resultats_phrase)
print("\n--- Tableau récapitulatif du racinage sur la phrase ---")
df_phrase
```

### Analyse ciblée de la famille lexicale de *"Consider"*
Observons spécifiquement comment les différentes formes dérivées du verbe *consider* sont harmonisées :
- `considering` $\rightarrow$ `consid`
- `considerable` $\rightarrow$ `consider` / `consid`
- `considerably` $\rightarrow$ `consider` / `consid`
- `considered` $\rightarrow$ `consid`

```python
# Filtrage sur les mots dérivés de "consider"
mots_consider = [row for row in resultats_phrase if "consid" in row["Porter Stem"].lower()]
pd.DataFrame(mots_consider)
```

## 6. Analyse Comparative & Visualisation Graphique
Pour quantifier l'impact de la racinisation sur la réduction du vocabulaire, comparons la taille du lexique unique avant et après traitement.

```python
# Analyse de la réduction lexicale
mots_uniques_originaux = len(set([t.lower() for t in tokens if t.isalnum()]))
mots_uniques_porter = len(set([row["Porter Stem"].lower() for row in resultats_phrase]))
mots_uniques_snowball = len(set([row["Snowball Stem"].lower() for row in resultats_phrase]))

stats_reduction = pd.DataFrame({
    "Étape": ["Vocabulaire Original", "Après PorterStemmer", "Après SnowballStemmer"],
    "Nombre de Mots Uniques": [mots_uniques_originaux, mots_uniques_porter, mots_uniques_snowball]
})

plt.figure(figsize=(8, 4.5))
bars = plt.bar(stats_reduction["Étape"], stats_reduction["Nombre de Mots Uniques"], color=['#64748b', '#2563eb', '#10b981'], width=0.55)
plt.title("Réduction de la Dimensionnalité Lexicale par Racinisation", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("Nombre de termes uniques", fontsize=11)
plt.ylim(0, mots_uniques_originaux + 3)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, int(yval), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()
```

## 7. Synthèse et Conclusion
1. **Efficacité de la Racinisation** : Le Stemming a permis de réduire la redondance lexicale en regroupant différentes déclinaisons d'une même racine sémantique (`considering`, `considerably`, `considered`).
2. **Porter vs Snowball** :
   - `PorterStemmer` est l'implémentation historique, rapide et robuste, mais parfois trop agressive ou rigide avec certaines terminaisons en `y` ou `ly`.
   - `SnowballStemmer` (Porter2) corrige ces imperfections, offre une meilleure cohérence linguistique et prend en charge nativement le multilinguisme (français, espagnol, allemand, arabe, etc.).
3. **Limites du Stemming** : Le radical obtenu (`consid`) n'est pas nécessairement un mot du dictionnaire (phénomène de *sur-racinisation* ou *under-stemming*). Pour préserver un mot orthographiquement valide, la **Lemmatisation** (`WordNetLemmatizer`) constitue l'alternative sémantique de choix.
