---
title: "Présentation : Fiabilité des Pipelines Big Data en Production"
subject: "Frameworks Big Data"
type: Présentation / Slides
tags:
  - 2mdsp
  - presentation
  - big-data
  - spark
  - orchestration
  - data-quality
  - data-lineage
  - site-reliability-engineering
date: 2026-10-07
---

# Fiabilité des Pipelines Big Data en Production
## Support de Présentation — Thème 4 : Au-delà d'Apache Spark : Les défis des systèmes Big Data modernes

> [!abstract] Guide du Présentateur (Presentation Guide)
> Ce document constitue un support de **slides interactives** complet, rédigé en français académique et professionnel, conforme aux standards de Master 2 Data Science & Big Data (2MDSP - ISLAI Béja).
> * Séparateurs de diapositives conformes : `---`.
> * Chaque diapositive inclut des **Notes de l'orateur (Speaker Notes)** détaillées pour vous guider lors de votre passage à l'oral face au professeur et à l'audience.

---

## Slide 1 : Titre & Cadrage Académique

### Fiabilité des Pipelines Big Data en Production
#### *Au-delà d'Apache Spark : Les défis des systèmes Big Data modernes*

> [!info] Fiche Académique
> * **Institution** : Institut Supérieur des Langues Appliquées et Informatique de Béja (ISLAI Béja)
> * **Formation** : Master 2 Data Science & Big Data (2MDSP)
> * **Module** : Frameworks Big Data
> * **Axe de Recherche** : Thème 4
> * **Auteur** : Étudiant en Master Data Science

```text
       ┌────────────────────────────────────────────────────────┐
       │   De la tolérance aux pannes d'infrastructure (Spark)  │
       │                         ▼                              │
       │   À l'ingénierie globale de la fiabilité des données   │
       │           (Data Reliability Engineering - DRE)         │
       └────────────────────────────────────────────────────────┘
```

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 minute
> * **Introduction** : "Bonjour Monsieur le Professeur, chers collègues. J'ai le plaisir de vous présenter aujourd'hui notre travail de recherche sur le Thème 4 en Frameworks Big Data : *La fiabilité des pipelines Big Data en production : Au-delà d'Apache Spark*."
> * **Message Clé** : "Pendant longtemps, le paradigme Big Data s'est focalisé sur la vitesse de calcul avec Apache Spark. Or, en environnement d'entreprise, faire tourner Spark ne garantit pas la validité des données. Aujourd'hui, nous allons répondre à la question essentielle : comment garantir la résilience et l'exactitude de nos flux du producteur au consommateur ?"

---

## Slide 2 : Modèle Mental — L'Analogie du Réseau Hydraulique

### Qu'est-ce qu'un "Pipeline de Données" et pourquoi la fiabilité est-elle vitale ?

![[assets/data_pipeline_water_analogy.svg|750]]

> [!info] Analogie du réseau hydraulique d'une métropole moderne :
> 1. **La Rivière Brute (Data Sources)** : flux ininterrompu d'événements (Kafka, CDC) charriant impuretés et sédiments imprévus.
> 2. **L'Usine de Traitement (Moteur Spark)** : puissance de calcul pour filtrer et transformer les volumes massifs.
> 3. **La Vanne de Sécurité & Laboratoire (Quality Gate & DLQ)** : isolement immédiat des échantillons contaminés avant pollution du réseau urbain.
> 4. **Réservoirs Purs & Robinets (Consommateurs / BI & ML)** : eau 100% conforme alimentant les dashboards stratégiques et les modèles d'IA.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * **Approche pédagogique** : "Pour poser le problème clairement, comparons un pipeline de données au réseau d'eau potable d'une ville."
> * **Démonstration** : "Spark est notre station de pompage géante. Mais le désastre survient si une eau polluée traverse l'usine et parvient aux robinets des habitants. En entreprise, cela équivaut à induire le comité de direction en erreur ou à empoisonner un modèle de machine learning."
> * **Idée force** : "La fiabilité ne réside pas seulement dans la puissance des pompes, mais dans la présence de vannes de sécurité et de bassins de quarantaine."

---

## Slide 3 : Problématique Centrale — Pourquoi Spark ne suffit-il pas en Production ?

### Les Limites du Modèle Classique (Beyond Spark Boundary)

![[assets/spark_boundary_vs_end_to_end_reliability.svg|750]]

> [!warning] Le Paradoxe de la Production :
> * **Excellence interne de Spark** : reconstruction autonome des partitions perdues via le graphe de lignage ($RDD\ Lineage$) lors du crash d'un nœud worker.
> * **Cécité sémantique externe (Semantic Blindness)** :
>   - Spark termine avec un succès technique parfait ($Exit\ Code\ 0$) même si 100% des lignes contiennent des prix négatifs ou des clés dupliquées.
>   - Incapacité d'auto-guérison globale lors d'un crash du Driver ($Driver\ OOM$).
>   - Vulnérabilité totale face aux dérives de schéma ($Schema\ Drift$) ou aux pannes d'APIs amont.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * **Remise en question** : "On entend souvent : 'Nous avons Spark et le RDD Lineage, pourquoi aurions-nous besoin d'autres architectures ?'"
> * **Explication** : "Comme l'illustre ce schéma, Spark gère uniquement ses pannes mémoire internes. Or, un pipeline réel traverse des systèmes hétérogènes (Kafka, APIs, bases relationnelles, Lakehouses). C'est pourquoi l'ingénierie moderne adopte les principes du **Data Reliability Engineering (DRE)**."

---

## Slide 4 : Les 4 Piliers Fondamentaux de la Recherche

### Feuille de route pour répondre aux questions du sujet

```text
                    ┌──────────────────────────────────────────────┐
                    │     Data Reliability Engineering (DRE)       │
                    └──────────────────────┬───────────────────────┘
                                           │
         ┌───────────────────┬─────────────┴───────┬───────────────────┐
         ▼                   ▼                     ▼                   ▼
   【 Pilier 1 】      【 Pilier 2 】        【 Pilier 3 】      【 Pilier 4 】
  Reprise Orchestr.   Surveillance Qualité  Traçabilité & Lignage  Dompter Retries
  Orchestration Rec.  Data Quality Gate     Lineage & Observ.      Resilient Patterns
  • State Backend     • 6 Dimensions        • 4 Piliers Observ.    • Retry Storms
  • K8s Pod Isolation • Circuit Breaker     • RCA Amont            • Exp. Backoff Jitter
  • Asset-Based Dags  • Pattern WAP         • Column-Level Lineage • ACID Idempotence
```

> [!tip] Objectif de la soutenance
> Présenter les solutions d'ingénierie concrètes adoptées par l'industrie pour chacun des 4 axes.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 minute
> * "Notre étude s'articule autour des 4 axes imposés :
>   1. Comment les orchestrateurs récupèrent-ils les tâches après un crash ?
>   2. Comment détecter automatiquement la corruption silencieuse ?
>   3. Comment le lignage accélère-t-il le diagnostic à la racine ?
>   4. Quels sont les dangers des retries naïfs et quelles sont les alternatives résilientes ?
>   Débutons par le premier axe."

---

## Slide 5 : Axe 1 — Reprise après Échec dans l'Orchestration

### Comment les orchestrateurs (Airflow, Dagster) garantissent-ils la résilience ?

$$G = (V, E) \quad \text{où } V \text{ représente les tâches, et } E \text{ les dépendances orientées}$$

> [!info] Les Fondements de la Reprise d'Orchestration
> 1. **Persistance d'État Découplée (External State Backend)** :
>    - Sauvegarde en temps réel des statuts (`QUEUED`, `RUNNING`, `SUCCESS`, `FAILED`, `UPSTREAM_FAILED`) dans un PostgreSQL indépendant.
>    - En cas de coupure de l'orchestrateur, aucun état historique n'est perdu.
> 2. **Reprise Granulaire Sélective (Fine-Grained Resume)** :
>    - Si la tâche 4 échoue après 3 tâches de plusieurs heures : **le DAG complet n'est jamais relancé** !
>    - L'orchestrateur relance uniquement la tâche défaillante et ses dépendances aval ($Downstream\ Only$), économisant des milliers d'euros de calcul Cloud.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "Dans Apache Airflow, un DAG est un graphe orienté acyclique. Le point capital est la dissociation entre le moteur d'exécution et la base de métadonnées."
> * "Grâce à cette séparation, un crash nocturne ne détruit pas le travail accompli. L'orchestrateur sait exactement où il s'est arrêté et reprend de manière ciblée."

---

## Slide 6 : Axe 1 Approfondi — Isolation Kubernetes & Approche par Actifs

### Isolation des Pods et Nouvelle Génération d'Orchestration

![[assets/orchestrator_dag_recovery_lifecycle.svg|750]]

> [!tip] Deux avancées architecturales majeures :
> * **Isolation par Conteneurs (KubernetesPodOperator)** :
>   - Exécution des jobs Spark lourds dans des pods K8s isolés avec quotas stricts (`Resource Limits`).
>   - Élimination des *tâches zombies* et protection du cluster de l'orchestrateur contre les crashs mémoire.
> * **Orchestration Déclarative par Actifs (Asset-Based Dagster)** :
>   - Remplacement de la vision impérative : *"Exécute le script A puis B"*
>   - Par la vision déclarative : *"Je veux l'actif `gold_revenue`, quels sont les actifs amont obsolètes (`Stale`) nécessitant un recalcul partiel ?"*

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "Ce diagramme illustre le cycle de reprise :
>   - Phase 1 : quand Spark tombe en OOM, l'orchestrateur bloque la tâche 4 en UPSTREAM_FAILED pour protéger les tables de production.
>   - Phase 2 : reprise ciblée du pod K8s avec allocation mémoire doublée (8Gi vers 16Gi), débloquant la suite du pipeline."

---

## Slide 7 : Axe 2 — Surveillance Automatisée de la Qualité des Données

### La Corruption Silencieuse et les 6 Dimensions Normatives

> [!danger] L'Angle Mort des Outils d'Infrastructure
> Des outils comme Datadog ou Prometheus surveillent le CPU et la RAM, mais sont **aveugles au contenu des tables** :
> Ils ne détectent pas la disparition de 50% des identifiants clients ou une baisse brutale de 80% du chiffre d'affaires !

![[assets/data_quality_six_dimensions_fr.svg|750]]

> [!info] Les 6 Dimensions Normatives de la Qualité (Standards DAMA & ISO 8000) :
> 1. **Complétude (Completeness)** : absence de valeurs manquantes sur les attributs critiques ($Null\ Ratio \le \epsilon$).
> 2. **Unicité (Uniqueness)** : unicité absolue des identifiants et clés primaires ($Primary\ Keys$).
> 3. **Validité (Validity)** : stricte conformité aux expressions régulières, formats et domaines de valeurs métiers.
> 4. **Cohérence (Consistency)** : conciliation parfaite des relations et clés étrangères inter-systèmes ($Cross-Table\ Accord$).
> 5. **Précision (Accuracy)** : exactitude arithmétique et fidélité de la donnée par rapport à la réalité d'entreprise ($Audit-Proof\ Precision$).
> 6. **Fraîcheur (Freshness / Timeliness)** : mise à disposition des données dans les fenêtres de latence prescrites ($SLA$).

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "Le pire cauchemar de l'ingénieur de données n'est pas le job qui s'arrête, mais le job qui réussit en produisant des données toxiques."
> * "Nous utilisons 6 dimensions standardisées : complétude, unicité, validité, cohérence, précision et fraîcheur, formalisées sous forme d'assertions de tests automatisés."

---

## Slide 8 : Axe 2 Architectural — Le Patron Coupe-Circuit (Circuit Breaker)

### Endiguer la propagation et isoler les données corrompues

![[assets/automated_data_quality_circuit_breaker.svg|750]]

> [!info] Composants du Disjoncteur de Données :
> 1. **Zone Bronze (Ingestion)** : réception brute des flux (Kafka / S3) et collecte des métriques d'entrée.
> 2. **Moteur d'Assertions (Validation)** : application des suites Great Expectations / Soda sur la couche Silver.
> 3. **Porte de Décision (Quality Gate)** :
>    - ✅ **Succès** : promotion des données saines vers la zone Gold certifiée.
>    - 🛑 **Échec** : ouverture du coupe-circuit, séquestration du lot dans une table de quarantaine (**DLQ / Quarantine Table**), alerte PagerDuty et gel des dashboards BI.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "Le principe du disjoncteur est inspiré du génie électrique : couper le circuit avant que la surtension ne détruise l'installation."
> * "Grâce à ce mécanisme, le décideur métier verra une donnée retardée mais jamais un chiffre corrompu qui induirait une fausse décision stratégique."

---

## Slide 9 : Axe 2 en Pratique — Le Pattern Write-Audit-Publish (WAP)

### Garanties Atomiques dans les Lakehouses Modernes (Iceberg & Delta Lake)

![[assets/write_audit_publish_wap_pattern.svg|750]]

> [!tip] Les 3 étapes du Pattern WAP :
> 1. **Écriture Isolée (WRITE)** : écriture dans une **branche de staging éphémère** sans impacter la branche `main`. Les consommateurs continuent d'interroger la production sans verrou.
> 2. **Audit Exhaustif (AUDIT)** : exécution de tous les tests de qualité et vérification de conformité de schéma directement sur la branche isolée.
> 3. **Publication ou Annulation (PUBLISH / ABORT)** :
>    - Succès $\rightarrow$ permutation atomique du pointeur de métadonnées (**Fast-Forward**) en une fraction de seconde (Zéro temps d'arrêt).
>    - Échec $\rightarrow$ suppression immédiate de la branche de staging (**Zéro lecture sale / Dirty Reads**).

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "Le pattern WAP calque la logique de Git sur les données : aucune fusion dans 'main' sans validation par le CI/CD."
> * "Dans Apache Iceberg, ce basculement atomique de métadonnées garantit qu'aucune donnée intermédiaire corrompue n'est jamais exposée."

---

## Slide 10 : Axe 3 — Lignage des Données et Observabilité

### Passer de la Spéculation au Diagnostic Chirurgical Instantané

![[assets/pipeline_observability_and_lineage.svg|700]]

> [!info] Les 4 Piliers de l'Observabilité des Données :
> * **Métriques** + **Logs** + **Traces** + **Lignage (Data Lineage)**.
> 
> * **Analyse Causale Amont (Upstream RCA)** :
>   Remonter les arêtes du graphe pour localiser l'origine exacte de la panne (ex: modification de type de colonne non annoncée dans PostgreSQL).
> * **Analyse du Rayon d'Impact Aval (Downstream Blast Radius)** :
>   Identifier tous les consommateurs, dashboards BI et modèles de Machine Learning impactés pour les geler préventivement.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "Dans une entreprise comptant des milliers de tables, chercher une erreur à la main est mission impossible."
> * "Le Data Lineage fournit la carte géographique complète du flux avec une vision amont (trouver la cause racine) et une vision aval (maîtriser le périmètre des dégâts)."

---

## Slide 11 : Axe 3 au Microscope — Lignage au Niveau des Colonnes

### La Précision Chirurgicale du Standard Ouvert OpenLineage

![[assets/column_level_lineage_graph.svg|750]]

> [!tip] Supériorité du Column-Level Lineage :
> * **Lignage de table** : signale seulement que `gold_kpi` a échoué à cause de `forex_rates`.
> * **Lignage de colonne** : analyse l'expression mathématique Spark :
>   $$\text{revenue\_usd} = \left(\frac{\text{amount\_cents}}{100.0}\right) \times \text{rate\_to\_usd}$$
>   et isole immédiatement la valeur `NULL` dans la colonne `rate_to_usd` sans perdre de temps à inspecter les millions de lignes d'utilisateurs ou de commandes. Réduit le MTTR de plusieurs heures à quelques secondes.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "Voici la pointe de l'observabilité : le Column-Level Lineage avec OpenLineage."
> * "Il inspecte l'AST (Abstract Syntax Tree) du code Spark et relie la formule au champ coupable en quelques secondes."

---

## Slide 12 : Axe 4 — Risques et Pathologies des Retries Naïfs

### Quand la politique de réessai aggrave la catastrophe !

![[assets/retry_mechanisms_and_failure_modes.svg|750]]

> [!danger] Les 3 Pathologies Meurtrières des Réessais Immédiats :
> 1. **Tempête de Réessais & Troupeau Tonitruant (Retry Storm & Thundering Herd)** :
>    Des délais d'attente fixes amènent des dizaines de workers à réattaquer simultanément une base de données surchargée, provoquant son crash complet.
> 2. **Opérations Non-Idempotentes & Écritures en Double** :
>    Réexécuter un `INSERT INTO` après une coupure transitoire crée des doublons et altère les états comptables : $f(f(x)) \neq f(x)$.
> 3. **La Pilule Empoisonnée (Poison Pill Data)** :
>    Erreur déterministe (cast invalide). Relancer 10 fois échouera 10 fois à coup sûr, gaspillant du budget Cloud en pure perte.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "L'option par défaut 'retries: 3' sans réflexion préalable est un piège destructeur."
> * "La partie gauche du schéma démontre comment des retries aveugles achèvent un serveur affaibli ou injectent des doublons destructeurs."

---

## Slide 13 : Axe 4 Ingénierie — Alternatives Résilientes aux Retries

### Backoff Exponentiel avec Gigue, Idempotence et Quarantaine

> [!tip] L'Arsenal Architectural Résilient :
> 1. **Décroissance Exponentielle avec Gigue (Exponential Backoff with Full Jitter)** :
>    $$t_{\text{wait}} = \min\left(t_{\text{max}},\, \mathcal{U}\left(0, t_{\text{base}} \cdot 2^{\text{attempt}}\right)\right)$$
>    Désynchronise les requêtes concurrentes et disperse la charge temporelle pour laisser la base guérir.
> 2. **Idempotence Stricte (ACID Lakehouse Idempotency)** :
>    Remplacer l'insertion simple par l'opération atomique `MERGE / UPSERT` dans Delta Lake et Iceberg :
>    $$f(f(x)) = f(x)$$
> 3. **Files de Messages Morts et Quarantaine (Dead Letter Queues - DLQ)** :
>    Interception des lignes toxiques dans une table `quarantine_data` tout en poursuivant le traitement fluide des millions de lignes saines.

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "La partie droite du schéma apporte les réponses d'ingénierie : le Full Jitter brise le troupeau tonitruant, le MERGE garantit l'idempotence, et la DLQ séquestre les pilules empoisonnées."

---

## Slide 14 : Matrice Comparative Synthétique

### Pratique Naïve vs Architecture de Production Résiliente

| Dimension d'Ingénierie | Pratique Naïve Classique | Architecture Résiliente de Production | Technologies de Référence |
| :--- | :--- | :--- | :--- |
| **Gestion de Reprise** | Relance intégrale du DAG depuis le début | Reprise sélective granulaire et pods K8s isolés | Airflow K8s, Dagster Assets |
| **Contrôle Qualité** | Audit manuel, ou réclamations utilisateurs | Contrôles d'assertions proactifs et disjoncteurs | Great Expectations, Soda Core |
| **Diagnostic Pannes** | Fouille artisanale dans des logs dispersés | Traçabilité au niveau colonne et graphes OpenLineage | OpenLineage, Marquez, DataHub |
| **Politique Réessai** | Réessais immédiats fixes (`Fixed Retries`) | Backoff exponentiel avec gigue + MERGE + DLQ | Backoff Jitter, Lakehouse, DLQ |
| **Protection Sorties** | Écritures directes dans les tables cibles | Pattern Write-Audit-Publish atomique (staging) | Apache Iceberg, Delta Branches |

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 2 minutes
> * "Ce tableau synthétise l'ensemble de notre étude : à chaque faille du modèle naïf répond une solution architecturale robuste adoptée par les géants de la Tech."

---

## Slide 15 : Synthèse, Bonnes Pratiques & Session Q&A

### Les 4 Règles d'Or du Data Reliability Engineer et Références

> [!tip] Les 4 Principes Directeurs :
> 1. **La Fiabilité se Conçoit Dès le Départ (Reliability by Design)** : concevoir chaque tâche pour être rigoureusement idempotente.
> 2. **Zéro Confiance envers les Données Entrantes (Zero-Trust Data)** : postuler la corruption a priori et valider à chaque étape.
> 3. **Lignage de Premier Rang (First-Class Lineage)** : intégrer OpenLineage pour effondrer le MTTR à quelques secondes.
> 4. **Dompter les Politiques de Retries** : imposer le Full Jitter et séquestrer les anomalies dans des Dead Letter Queues.

> [!info] Références Bibliographiques Majeures
> * **Reis, J., & Housley, M.** (2022). *Fundamentals of Data Engineering*, O'Reilly Media.
> * **Moses, B., & Koren, L.** (2022). *Data Quality Fundamentals*, O'Reilly Media.
> * **Armbrust, M., et al.** (2020). *Delta Lake: High-Performance ACID Table Storage*, VLDB.
> * **OpenLineage Standard** : *openlineage.io*.

### Merci pour votre attention — Place aux questions (Session Q&A)

> [!quote] Notes de l'orateur (Speaker Notes) — Durée : 1 minute
> * "En conclusion, la fiabilité n'est pas un luxe mais la condition sine qua non de toute valeur créée par le Big Data et l'IA. Je vous remercie pour votre attention et je me tiens à votre entière disposition pour répondre à vos questions."
