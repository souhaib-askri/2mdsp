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

# TP1 – Initiation au Traitement de Données Big Data avec PySpark dans un Environnement Cloud

## 1. Objectifs du TP
Le traitement des données massives (**Big Data**) requiert des architectures distribuées capables de traiter des volumes de données importants avec une grande rapidité. Ce TP simule un **mini-environnement Cloud Big Data** en exploitant Python et **Apache Spark (PySpark)** sur une infrastructure Cloud (Google Colab ou environnement local émulé).

### Objectifs d'apprentissage :
1. **Configuration de l'environnement** : Installer et initialiser une session Apache Spark (`SparkSession`).
2. **Ingestion & Structuration** : Générer et charger un jeu de données structuré (`cities.csv`) dans un DataFrame Spark distribué.
3. **Exploration des Métadonnées (EDA)** : Inspecter le schéma, vérifier les types de données et quantifier les enregistrements.
4. **Transformations & Traitement Distribué** : Appliquer les transformations Spark (`filter`, `groupBy`, `agg`, `orderBy`).
5. **Persistance & Stockage Cloud** : Exporter les résultats aux formats CSV et Parquet simulant un stockage objet Cloud (ex. Google Drive / AWS S3).
6. **Audit de l'Environnement d'Exécution** : Collecter les métriques système (OS, processeur, version de Python) de la machine Cloud.


## 2. Installation & Initialisation de l'Environnement
Dans un environnement de type Cloud (comme Google Colab), Apache Spark et PySpark doivent être installés dans la machine virtuelle active.

```python
# Installation de PySpark si non présent dans l'environnement
# !pip install pyspark
```

```python
import os
import sys
import platform
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Imports essentiels d'Apache Spark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, desc, round as spark_round
```

### Initialisation de la SparkSession
La `SparkSession` est le point d'entrée unifié pour programmer Spark avec l'API DataFrame et Dataset. Elle encapsule le contexte Spark (`SparkContext`), les paramètres de configuration et le moteur d'exécution distribué.

```python
# Création et configuration de la session Spark locale / cloud
spark = SparkSession.builder \
    .appName("TP1_Cloud_BigData_PySpark") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Vérification du bon fonctionnement et affichage des métadonnées Spark
print(f"Version d'Apache Spark : {spark.version}")
print(f"Nom de l'application   : {spark.sparkContext.appName}")
print(f"Master URL             : {spark.sparkContext.master}")
spark
```

## 3. Préparation du Jeu de Données (`cities.csv`)
Pour simuler une ingestion de données climatiques ou urbaines, nous créons un fichier CSV contenant les colonnes :
- `id` : Identifiant unique de la ville.
- `city` : Nom de la métropole.
- `temperature` : Température mesurée en degrés Celsius (°C).
- `country` : Pays (attribut contextuel enrichi).

```python
# Définition des données synthétiques
csv_data = """id,city,temperature,country
1,Tunis,24.5,Tunisia
2,Paris,18.2,France
3,London,15.8,United Kingdom
4,Tokyo,21.0,Japan
5,New York,19.4,USA
6,Cairo,29.8,Egypt
7,Montreal,12.3,Canada
8,Dubai,35.2,UAE
9,Rome,23.1,Italy
10,Madrid,25.6,Spain
"""

# Création du fichier CSV localement
csv_path = "cities.csv"
with open(csv_path, "w", encoding="utf-8") as f:
    f.write(csv_data)

print(f"Fichier '{csv_path}' créé avec succès.")
```

### Ingestion du CSV dans un DataFrame PySpark
Nous chargeons le fichier en activant l'inférence automatique de schéma (`inferSchema=True`) et la détection de la ligne d'en-tête (`header=True`).

```python
# Chargement des données dans Spark
df_cities = spark.read.csv(csv_path, header=True, inferSchema=True)

# Affichage des premières lignes du DataFrame
print("Aperçu des données chargées :")
df_cities.show(truncate=False)
```

## 4. Exploration et Analyse des Métadonnées (EDA)
Avant toute manipulation, nous analysons la structure et les propriétés statistiques fondamentales du DataFrame distribué.

```python
# 1. Schéma du DataFrame (Types de données et nullabilité)
print("--- Schéma Spark ---")
df_cities.printSchema()

# 2. Nombre total de lignes et colonnes
num_rows = df_cities.count()
num_cols = len(df_cities.columns)
print(f"\nDimensions du jeu de données : {num_rows} lignes x {num_cols} colonnes.")

# 3. Liste des noms de colonnes
print(f"Colonnes disponibles : {df_cities.columns}")

# 4. Résumé statistique numérique
print("\n--- Statistiques descriptives de la température ---")
df_cities.describe("temperature").show()
```

## 5. Traitement & Transformations Distribuées

### A. Calcul de la Température Moyenne Globale
Nous exploitons les fonctions d'agrégation de PySpark pour extraire la température moyenne de l'ensemble des villes.

```python
# Calcul de la moyenne globale
avg_temp_val = df_cities.select(spark_round(avg("temperature"), 2).alias("avg_temp")).collect()[0]["avg_temp"]
print(f"Température moyenne globale : {avg_temp_val} °C")
```

### B. Filtrage des Villes avec Température > 22 °C
Nous appliquons la transformation `filter()` (ou `where()`) pour isoler les métropoles dont le climat dépasse le seuil critique de 22 °C.

```python
# Filtrage selon le critère : temperature > 22
df_filtered = df_cities.filter(col("temperature") > 22.0)

print("Villes avec température > 22 °C :")
df_filtered.show()
```

### C. Tri Décroissant par Température
Nous ordonnons les enregistrements filtrés de la température la plus élevée à la plus basse à l'aide de `orderBy(desc("temperature"))`.

```python
# Tri décroissant
df_sorted = df_filtered.orderBy(desc("temperature"))

print("Villes filtrées classées par ordre décroissant de température :")
df_sorted.show()
```

## 6. Visualisation Graphique des Données
Pour analyser intuitivement les écarts de température observés, nous convertissons le sous-ensemble Spark en DataFrame Pandas afin de générer une visualisation avec Seaborn et Matplotlib.

```python
# Conversion vers Pandas pour la visualisation locale
pdf_all = df_cities.orderBy(desc("temperature")).toPandas()

plt.figure(figsize=(10, 5))
palette = ['#e11d48' if t > 22 else '#2563eb' for t in pdf_all['temperature']]
bars = sns.barplot(data=pdf_all, x="city", y="temperature", palette=palette)

# Ligne de seuil à 22°C et ligne de moyenne
plt.axhline(22, color='#e11d48', linestyle='--', linewidth=1.5, label='Seuil critique (22 °C)')
plt.axhline(avg_temp_val, color='#10b981', linestyle=':', linewidth=1.5, label=f'Moyenne globale ({avg_temp_val} °C)')

plt.title("Distribution des Températures par Ville (Simulation Big Data)", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Villes", fontsize=11)
plt.ylabel("Température (°C)", fontsize=11)
plt.xticks(rotation=30)
plt.legend()
plt.tight_layout()
plt.show()
```

## 7. Sauvegarde des Résultats & Simulation de Stockage Cloud

Dans une architecture Big Data Cloud réelle :
- Les jeux de données transformés sont sérialisés vers des formats colonnaires optimisés comme **Apache Parquet**.
- Les fichiers sont sauvegardés soit sur un volume persistant local (`/content/results`), soit exportés vers un service de stockage Cloud comme Google Drive ou AWS S3.

```python
# Création du répertoire de résultats
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)

# 1. Sauvegarde au format CSV avec en-tête
csv_output_path = os.path.join(output_dir, "cities_filtered_csv")
df_sorted.coalesce(1).write.mode("overwrite").option("header", "true").csv(csv_output_path)
print(f"DataFrame sauvegardé avec succès en CSV sous : {csv_output_path}")

# 2. Sauvegarde au format Parquet (standard industriel Big Data)
parquet_output_path = os.path.join(output_dir, "cities_filtered_parquet")
df_sorted.coalesce(1).write.mode("overwrite").parquet(parquet_output_path)
print(f"DataFrame sauvegardé avec succès en Parquet sous : {parquet_output_path}")
```

```python
# Vérification des fichiers générés
for root, dirs, files in os.walk(output_dir):
    for file in files:
        if not file.startswith("."):
            print("Fichier exporté :", os.path.join(root, file))
```

<!-- #region -->
### Note sur la sauvegarde sur Google Drive (Environnement Colab) :
Dans Google Colab, la persistance permanente s'effectue en montant Google Drive :
```python
# from google.colab import drive
# drive.mount('/content/drive')
# df_sorted.coalesce(1).write.mode("overwrite").parquet('/content/drive/MyDrive/BigData_Results/cities_filtered')
```
<!-- #endregion -->

## 8. Analyse de l'Environnement d'Exécution Cloud
Conformément aux exigences du TP, nous inspectons l'environnement d'exécution pour documenter la machine hôte et les versions des composants logiciels.

```python
print("=" * 60)
print("AUDIT DE L'ENVIRONNEMENT D'EXÉCUTION CLOUD / SYSTÈME")
print("=" * 60)
print(f"Système d'exploitation (OS) : {platform.system()} {platform.release()} ({platform.version()})")
print(f"Architecture machine        : {platform.machine()}")
print(f"Nom de l'hôte (Node name)   : {platform.node()}")
print(f"Version de Python           : {sys.version.split()[0]}")
print(f"Interpréteur Python         : {sys.executable}")
print(f"Version Apache Spark        : {spark.version}")
print(f"Nombre de cœurs alloués     : {spark.sparkContext.defaultParallelism}")
print("=" * 60)
```

## 9. Conclusion & Synthèse
Ce premier travail pratique a permis de concrétiser les concepts fondamentaux du cours d'**Environnement Cloud pour le Big Data** :
1. **Abstraction de l'Infrastructure** : Déploiement et exécution de Spark sans configuration lourde de clusters physiques.
2. **Paradigme de Traitement Distribué** : L'API DataFrame de PySpark applique des plans d'exécution optimisés (Catalyst Optimizer) pour exécuter des requêtes de filtrage et d'agrégation.
3. **Format Colonnaire vs Fichier Plat** : Compréhension de la sérialisation des sorties pour le stockage persistant dans le Cloud.
