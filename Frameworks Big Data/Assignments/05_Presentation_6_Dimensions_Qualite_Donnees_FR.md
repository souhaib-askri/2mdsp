---
title: "Présentation : Les 6 Dimensions Normatives de la Qualité des Données"
subject: "Frameworks Big Data"
type: Présentation / Slides
tags:
  - 2mdsp
  - presentation
  - big-data
  - data-quality
  - dama
  - iso-8000
  - circuit-breaker
  - great-expectations
date: 2026-10-07
---

# Les 6 Dimensions Normatives de la Qualité des Données
## Cadre Méthodologique DAMA & ISO 8000 pour les Pipelines Big Data en Production

> [!abstract] Guide du Présentateur
> Ce support de présentation détaille de façon approfondie les **6 dimensions de la qualité des données**, leur formalisation mathématique, les risques métiers associés et leur mise en œuvre technique (assertions Great Expectations, architecture coupe-circuit et pattern WAP).
> * Séparateurs de diapositives : `---`.
> * Inclut des notes de l'orateur complètes pour chaque slide.

---

## Slide 1 : Titre & Introduction

### Les 6 Dimensions Normatives de la Qualité des Données
#### *Cadre Méthodologique DAMA & ISO 8000 pour les Pipelines Big Data en Production*

> [!info] Cadrage Académique
> * **Formation** : Master 2 Data Science & Big Data (2MDSP) — ISLAI Béja
> * **Module** : Frameworks Big Data
> * **Focus** : Ingénierie de la Fiabilité & Détection de la Corruption Silencieuse

```text
       ┌────────────────────────────────────────────────────────┐
       │   Surveillance des Machines (CPU/RAM/Exit Code 0)      │
       │                         ▼                              │
       │   Surveillance Sémantique du Contenu des Données       │
       │           (Les 6 Dimensions DAMA / ISO 8000)           │
       └────────────────────────────────────────────────────────┘
```

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 minute
> "Bonjour Monsieur le Professeur, chers collègues. Aujourd'hui, nous explorons les 6 dimensions normatives de la qualité des données en environnement Big Data, et comment les transformer en barrières de sécurité automatisées au sein de nos pipelines."

---

## Slide 2 : Problématique — L'Angle Mort et la Corruption Silencieuse

### Pourquoi la surveillance traditionnelle d'infrastructure est-elle aveugle ?

> [!danger] Le Piège de la Surveillance d'Infrastructure
> Des outils comme Prometheus ou Datadog surveillent le cluster Spark :
> * *Verdict technique* : "Charge CPU optimale, mémoire stable, Exit Code 0 !"
> * *Réalité métier* :
>   - 80% des prix d'achats sont négatifs.
>   - 50 000 transactions ont un `user_id` nul (`NULL`).
>   - Les dates ont muté de format sans avertissement.
>   - **Conséquence** : Les rapports stratégiques sont faussés sans aucune alerte technique !

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> "La pire défaillance n'est pas le job qui s'interrompt avec une erreur explicite, mais le job qui s'exécute avec succès en propageant une donnée corrompue. C'est ce qu'on appelle la corruption silencieuse."

---

## Slide 3 : Architecture Globale — Les 6 Dimensions Normatives

### Schéma Structurel d'Évaluation de la Qualité

![[assets/data_quality_six_dimensions_fr.svg|750]]

> [!info] Les 6 Branches du Cadre Qualité (DAMA / ISO 8000) :
> 1. **Complétude (Completeness)** : absence d'attributs obligatoires manquants ($Null\ Ratio \le \epsilon$).
> 2. **Unicité (Uniqueness)** : stricte unicité des entités ($Distinct == Count$).
> 3. **Validité (Validity)** : conformité aux règles de domaine, formats et regex.
> 4. **Cohérence (Consistency)** : conciliation parfaite des données inter-systèmes.
> 5. **Précision (Accuracy)** : exactitude et fidélité à la réalité observée ($\Delta < \delta$).
> 6. **Fraîcheur (Freshness)** : respect des délais temporels d'arrivée ($Lag \le SLA$).

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> "Ce schéma présente la structure globale : chaque dimension correspond à une métrique précise, un test automatisé dans des outils comme Great Expectations, et prévient un risque d'entreprise majeur."

---

## Slide 4 : Dimension 1 — La Complétude (Completeness)

### Traquer l'absence de valeurs obligatoires

> [!tip] Formalisation & Métrique
> $$\text{Null\_Ratio}(A) = \frac{\text{Count}(\text{rows where } A \text{ is NULL})}{\text{Total\_Rows}} \le \epsilon$$

* **Risque Métier** : Chute brutale des taux de conversion, rupture catastrophique des jointures `INNER JOIN`, rejet des données par les modèles de Machine Learning.
* **Exemples** : Identifiant client manquant, montant d'achat à blanc, code pays vide.
* **Test Automatisé (Great Expectations)** :
  ```python
  validator.expect_column_values_to_not_be_null(column="customer_id")
  validator.expect_column_null_ratio_to_be_between(column="discount", min_value=0.0, max_value=0.05)
  ```

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 min 30 s
> "En Big Data, une clé primaire devenue NULL élimine silencieusement des millions de lignes lors d'un simple INNER JOIN en aval."

---

## Slide 5 : Dimension 2 — L'Unicité (Uniqueness)

### Éliminer les doublons et les écritures parasites

> [!tip] Formalisation & Métrique
> $$\text{Distinct}(\text{Key}) = \text{Total\_Rows}$$

* **Risque Métier** : Facturation double des clients, gonflements artificiels des volumes d'activité, explosion combinatoire des jointures (produits cartésiens non maîtrisés).
* **Causes Types** : Réessais aveugles (Retries sur requêtes `INSERT INTO`), sémantique *At-least-once* non dédupliquée dans Kafka.
* **Test Automatisé** :
  ```python
  validator.expect_column_values_to_be_unique(column="transaction_id")
  ```
* **Solution Architecturale** : Utilisation stricte de l'opération atomique **MERGE INTO (Upsert)** dans Delta Lake ou Apache Iceberg.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 min 30 s
> "L'unicité est violée lorsque les réessais d'orchestration ne sont pas idempotents. Remplacer INSERT par MERGE est le remède absolu."

---

## Slide 6 : Dimension 3 — La Validité (Validity)

### Respecter les domaines de définition et les structures

> [!tip] Formalisation & Typologie
> La valeur doit appartenir au domaine de validité défini : $x \in \mathcal{D}$ ou respecter une expression régulière $R$.

* **Risque Métier** : Crash des calculs lors des conversions de types numériques, blocage des interfaces clientes, non-conformité réglementaire (RGPD).
* **Exemples** : Prix négatif ($-50\ €$), adresse email sans arobase, code pays inexistant, âge supérieur à 150 ans.
* **Test Automatisé** :
  ```python
  validator.expect_column_values_to_be_between(
      column="unit_price", min_value=0.01, max_value=1000000.00
  )
  validator.expect_column_values_to_match_regex(
      column="email", regex=r"^[^@]+@[^@]+\.[^@]+$"
  )
  ```

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 min 30 s
> "La validité bloque les 'pilules empoisonnées' : des chaînes de caractères corrompues qui feraient planter un cast Spark."

---

## Slide 7 : Dimension 4 — La Cohérence (Consistency)

### Garantir l'harmonie et l'intégrité inter-systèmes

> [!tip] Formalisation & Règle
> Concordance parfaite entre systèmes hétérogènes : $\text{Cross-System Drift} = 0$.

* **Risque Métier** : Enregistrements orphelins (ex: commande faisant référence à un client inexistant), divergence entre le stock physique et le grand livre comptable.
* **Spécificité Big Data** : Les systèmes de stockage distribués (S3, HDFS) n'imposent pas de contraintes physiques de clés étrangères (Foreign Keys) pour préserver la scalabilité.
* **Test Automatisé (Soda / dbt)** :
  ```yaml
  # Test de relation dbt
  - name: order_items
    columns:
      - name: order_id
        tests:
          - relationships:
              to: ref('orders')
              field: id
  ```

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 min 30 s
> "Puisque les Lakehouses ne vérifient pas les clés étrangères au niveau du stockage, c'est au pipeline de vérifier la cohérence avant publication."

---

## Slide 8 : Dimension 5 — La Précision (Accuracy)

### La fidélité par rapport à la réalité observable

> [!tip] Formalisation & Métrique
> Mesure de l'écart vis-à-vis de la vérité certifiée (Golden Record) : $|\text{Valeur} - \text{Vérité}| < \delta$.

* **Risque Métier** : Pertes financières par arrondi fautif, dérive de calibration de capteurs IoT, erreurs d'échelle (ex: unité en centimes interprétée en euros).
* **Exemples** : Taux de change appliqué sans décimales, quantité physique enregistrée à $0.00$.
* **Test Automatisé** :
  ```python
  validator.expect_column_mean_to_be_between(column="measured_voltage", min_value=228.0, max_value=232.0)
  validator.expect_column_stdev_to_be_between(column="sensor_temp", min_value=1.0, max_value=4.0)
  ```

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 min 30 s
> "Une donnée peut être valide syntaxiquement tout en étant fausse. La précision mesure l'exactitude de la mesure."

---

## Slide 9 : Dimension 6 — La Fraîcheur & Ponctualité (Freshness / Timeliness)

### Le respect des engagements temporels (SLAs)

> [!tip] Formalisation & Métrique
> $$\text{Latence} = T_{\text{actuel}} - \max(T_{\text{événement}}) \le \text{SLA}$$

* **Risque Métier** : Décisions stratégiques fondées sur des données périmées, alertes anti-fraude en retard, tableau de bord gelé sans notification.
* **Causes Courantes** : Blocage silencieux d'un connecteur CDC, accumulation de retard (Lag) sur Kafka, échec d'un job de nuit non supervisé.
* **Test Automatisé (Soda Core)** :
  ```yaml
  checks for orders:
    - freshness(order_timestamp) < 2h
  ```

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 min 30 s
> "La fraîcheur répond à la question : 'Cette donnée est-elle encore d'actualité ?' Une donnée parfaite livrée avec 6 heures de retard perd toute sa valeur."

---

## Slide 10 : Mise en Œuvre — Le Disjoncteur Automatisé (Circuit Breaker)

### Transformer les 6 dimensions en barrières d'exécution

![[assets/automated_data_quality_circuit_breaker.svg|750]]

> [!info] Cycle d'Exécution du Coupe-Circuit :
> 1. **Ingestion Bronze** : capture brute des données et profils statistiques initiaux.
> 2. **Évaluation Silver** : exécution des tests sur les 6 dimensions.
> 3. **Décision** :
>    - Si 100% des tests critiques sont validés $\rightarrow$ Passage vers la couche Gold.
>    - Si échec $\rightarrow$ Ouverture du disjoncteur, routage vers la table de quarantaine (**Dead Letter Queue - DLQ**), gel des dashboards et notification d'astreinte.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> "Les 6 dimensions ne sont pas théoriques : elles arment le disjoncteur. Si un test échoue, la donnée toxique est isolée dans la DLQ sans contaminer la production."

---

## Slide 11 : Garantie Atomique — Le Pattern Write-Audit-Publish (WAP)

### Éliminer les lectures sales dans les Lakehouses (Iceberg & Delta Lake)

![[assets/write_audit_publish_wap_pattern.svg|750]]

> [!tip] Déroulement du Pattern WAP :
> * **1. WRITE** : Écriture sur une branche de staging éphémère sans impacter `main`.
> * **2. AUDIT** : Exécution exhaustive des contrôles des 6 dimensions sur la branche temporaire.
> * **3. PUBLISH / ABORT** :
>   - Succès : Permutation atomique du pointeur de métadonnées (Fast-Forward sans temps d'arrêt).
>   - Échec : Destruction de la branche éphémère (Zéro lecture sale / Zero Dirty Reads).

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> "Le pattern WAP calque le modèle Git sur les données : aucune fusion dans 'main' avant validation complète des 6 dimensions."

---

## Slide 12 : Conclusion & Recommandations

### Les 4 Piliers d'une Stratégie Qualité Industrielle

> [!tip] Règles Directrices pour l'Ingénieur de Données
> 1. **Contrats de Données (Data Contracts)** : Formaliser les 6 dimensions comme des engagements mutuels entre producteurs et consommateurs.
> 2. **Automatisation Systématique** : Aucune donnée ne franchit la couche Gold sans validation par un moteur déclaratif (Great Expectations, Soda).
> 3. **Isolation et Continuité** : Utiliser des coupes-circuits et des files de quarantaine (DLQ) pour ne pas bloquer les données saines.
> 4. **Auditabilité et Traçabilité** : Associer chaque rejet de qualité au lignage OpenLineage pour isoler la cause racine en temps réel.

### Merci pour votre attention — Session de Questions-Réponses (Q&A)

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 minute
> "En conclusion, sans qualité rigoureuse, les projets de Big Data et d'IA reposent sur du sable. Je vous remercie pour votre attention et je suis prêt à répondre à vos questions."
