---
title: Speech de la présentation – Fiabilité des pipelines Big Data
subject: Frameworks Big Data
type: Cours
tags:
  - 2mdsp
  - big-data
  - pipelines
date: 2026-10-07
---

# Speech : Fiabilité des pipelines Big Data en production

> [!info] Mode d'emploi
> - Durée totale visée : **≈ 18 à 20 minutes** (20 diapositives, ≈ 1 min chacune).
> - Les indications entre crochets *[geste / transition]* ne se disent pas à voix haute.
> - Si vous êtes plusieurs : répartition suggérée en **4 blocs** (voir la fin du document).
> - Support : [[06_Presentation_Fiabilite_Pipelines_Brutalisme_FR.pptx]]

---

## Diapositive 1 — Titre (≈ 0:30)

Bonjour à toutes et à tous. Aujourd'hui, nous allons parler de la **fiabilité des pipelines Big Data en production**.

Construire un pipeline qui fonctionne une fois est facile. Le faire fonctionner correctement, tous les jours, malgré les pannes, les erreurs de données et les changements de schéma, c'est un tout autre défi. C'est ce que nous allons explorer.

## Diapositive 2 — Sommaire : quatre axes, quatre questions (≈ 1:00)

Notre exposé s'organise autour de **quatre questions**, une par axe :

1. **Récupérer** : comment les systèmes d'orchestration récupèrent-ils les tâches après une défaillance ?
2. **Prévenir** : comment surveiller automatiquement la qualité des données ?
3. **Diagnostiquer** : comment le lignage et l'observabilité facilitent-ils le diagnostic des erreurs ?
4. **Compléter** : quelles sont les limites des mécanismes de reprise basés sur les retries ?

Mais d'abord, deux diapositives de contexte pour poser les bases.

## Diapositive 3 — Qu'est-ce qu'un pipeline de données ? (≈ 1:15)

Un pipeline de données est une **séquence automatisée d'étapes** qui déplace des données depuis des sources (bases opérationnelles, journaux, API, capteurs IoT) vers une destination, en les transformant en route pour l'analyse, le reporting ou le machine learning.

L'image à retenir est celle de la **chaîne de production** : chaque maillon reçoit, transforme et transmet. Et comme dans une usine, une défaillance à un endroit se répercute sur **tout ce qui est en aval**.

Le contexte Big Data rend cette chaîne exigeante : ce sont les **5 V**.
- **Volume** : des téraoctets ou pétaoctets, donc des moteurs distribués comme Spark ou Flink, et tout recalcul complet est coûteux.
- **Vélocité** : des flux continus, avec une faible latence.
- **Variété** : des formats et des schémas qui évoluent sans prévenir.
- **Véracité** : des données incomplètes, dupliquées ou erronées.
- **Valeur** : seules des données correctes et à jour produisent de la valeur.

## Diapositive 4 — Les 5 étapes et le défi de la fiabilité (≈ 1:15)

Un pipeline se décompose en **cinq étapes** : l'ingestion, le traitement, le stockage, l'exposition et l'orchestration. Pour chacune, on voit les technologies courantes et, point important pour la suite, les **défaillances typiques** : une source indisponible à l'ingestion, une erreur de mémoire (OOM) ou un déséquilibre des données (*skew*) au traitement, des écritures partielles au stockage, des chiffres erronés à l'exposition, un scheduler arrêté ou une tâche zombie à l'orchestration.

Un pipeline fiable doit livrer des données **correctes, complètes, à l'heure** (selon les SLA) et **répétables**. Les sources de panne sont multiples : infrastructure, logiciel, données et même organisation. C'est pourquoi nous allons étudier quatre réponses complémentaires.

---

## Axe 1 — Récupérer *(≈ 5 min)*

### Diapositive 5 — Comment les orchestrateurs récupèrent-ils les tâches ? (≈ 1:15)

Le principe fondamental : l'orchestrateur **sépare l'état du pipeline, qui est persisté, de l'exécution, qui est éphémère**. Un worker peut disparaître à tout moment, mais l'état de chaque tâche reste enregistré dans une base de métadonnées durable. L'orchestrateur n'a donc pas besoin que le processus défaillant lui explique ce qui s'est passé : il relit l'état et décide.

C'est pour cela qu'Airflow, Dagster ou Prefect modélisent un pipeline sous forme de **DAG**, un graphe orienté acyclique : chaque nœud est une tâche avec un état, chaque arête une dépendance. Reprendre après une panne, c'est retrouver les nœuds qui ne sont pas « réussis » et les rejouer, ainsi que leurs descendants.

En bas, les états d'une tâche dans Airflow : *scheduled*, *running*, *success*, *failed*, *up_for_retry*, *upstream_failed* et *skipped*.

### Diapositive 6 — Les 5 étapes de la reprise (≈ 1:15)

La reprise suit cinq étapes.

1. **Persistance** : chaque transition d'état est écrite en base, c'est le journal de référence.
2. **Détection** : trois mécanismes. L'**échec explicite** (exception, code de sortie non nul) ; l'**absence de heartbeat**, car un processus mort ne peut pas signaler sa propre panne, la tâche devient alors « zombie » ; et le **timeout**, qui interrompt une tâche bloquée.
3. **Décision** : le scheduler applique la politique de retry.
4. **Replanification** : la tâche retourne en file d'attente et peut s'exécuter sur **un autre worker**.
5. **Propagation contrôlée** : les tâches dépendantes attendent ; si l'échec est définitif, elles passent en *upstream_failed* au lieu de traiter des données incomplètes.

### Diapositive 7 — Politique de retry : backoff et jitter (≈ 1:00)

Pour la décision de reprise, deux techniques clés. Le **backoff exponentiel** allonge le délai à chaque échec (2, 4, 8 minutes) pour laisser le temps au système défaillant de se rétablir. Le **jitter** ajoute de l'aléa, pour que des centaines de tâches échouées au même moment ne se relancent pas toutes à la même seconde.

À droite, un exemple de configuration Airflow dans `default_args` : trois tentatives, délai initial, backoff exponentiel, délai maximal, timeout d'exécution et un callback d'alerte après le dernier échec.

### Diapositive 8 — Reprise ciblée et approches alternatives (≈ 1:00)

On ne veut pas toujours tout rejouer. Trois outils : le **clear** d'Airflow, qui rejoue seulement la tâche échouée et ses descendantes ; le **backfill**, pour rejouer une période historique, par exemple après la correction d'un bug, à condition que les tâches soient paramétrées par leur fenêtre temporelle ; et le **repair run** de Databricks.

Le tableau montre d'autres approches : l'état par tâche, l'**event sourcing** de Temporal, le **checkpointing** de Spark Streaming et Flink, et le **lignage de calcul** de Spark. Elles se combinent : un orchestrateur pour l'enchaînement global, le checkpointing du moteur pour la reprise à l'intérieur d'un job.

### Diapositive 9 — Idempotence et résilience de l'orchestrateur (≈ 1:15)

La reprise rejoue du code. Il faut donc que les tâches soient **idempotentes** : l'exécuter une fois ou dix fois donne le même résultat. En pratique : `INSERT OVERWRITE` par partition, `MERGE` sur une clé métier, commit atomique avec Delta Lake ou Iceberg, et tâches paramétrées par leur fenêtre temporelle.

> [!tip] Message à retenir
> L'orchestrateur garantit au mieux « **au moins une fois** ». Avec des écritures idempotentes, on obtient en pratique « **exactement une fois** ».

En bas, la résilience de l'orchestrateur lui-même : plusieurs schedulers en haute disponibilité, redémarrage sans perte, exécuteurs distribués, et surtout la **base de métadonnées**, composant critique qui contient toute la mémoire du système et doit être sauvegardée et répliquée.

---

## Axe 2 — Prévenir *(≈ 3:30)*

### Diapositive 10 — Surveiller automatiquement la qualité des données (≈ 1:15)

Un pipeline peut s'exécuter sans erreur et produire des résultats faux : une source qui envoie la moitié des lignes, une colonne qui change d'unité, une jointure qui duplique. L'orchestrateur voit une tâche verte, alors que le résultat est inutilisable. La surveillance de la qualité comble l'écart entre **succès technique** et **succès fonctionnel**.

Le principe : traiter les données comme du code, les tester à chaque exécution. On contrôle **sept dimensions** : complétude, unicité, validité, fraîcheur, volumétrie, distribution et schéma.

### Diapositive 11 — Où contrôler et avec quels outils ? (≈ 1:15)

Trois points de contrôle : **à l'ingestion**, car une donnée rejetée tôt coûte peu ; **entre les transformations**, pour vérifier les invariants comme le nombre de lignes avant et après une jointure ; et **avant la publication**, dernière barrière avant la BI et le ML.

Côté outils : Great Expectations, Soda, dbt tests, Deequ, Pandera. Côté pratiques :
- les **quality gates** : le pipeline s'arrête ou met le lot en quarantaine si un contrôle critique échoue ;
- la **détection d'anomalies** avec des seuils dynamiques ;
- les **data contracts**, accord entre producteur et consommateur validé en intégration continue ;
- la **gravité graduée**, pour distinguer bloquant et avertissement et éviter la fatigue d'alerte.

### Diapositive 12 — Barrière de qualité et indicateurs (≈ 1:00)

Voici une quality gate concrète dans Airflow : un `SQLTableCheckOperator` vérifie que la table n'est pas vide et qu'il n'y a pas de doublons sur `order_id`. Grâce à `load >> quality_gate >> publish`, la publication ne s'exécute que si le contrôle réussit, par la règle `all_success`.

Pour piloter la qualité dans le temps : le **MTTD**, temps moyen de détection ; le **MTTR**, temps moyen de résolution ; et le **data downtime**, la durée pendant laquelle les données sont manquantes, erronées ou périmées.

---

## Axe 3 — Diagnostiquer *(≈ 3:30)*

### Diapositive 13 — Le lignage des données (≈ 1:15)

Dans un pipeline, une erreur apparaît rarement là où elle est née. Le **lignage** cartographie les dépendances entre sources, transformations et consommateurs. Il permet deux analyses :
- **vers l'amont** : l'analyse de cause racine, de la donnée erronée jusqu'à la source fautive ;
- **vers l'aval** : l'analyse d'impact, pour savoir qui prévenir et quoi rejouer. C'est aussi utile pour la conformité, par exemple le RGPD.

La granularité compte : le lignage au niveau **table** est trop grossier, alors que le niveau **colonne** isole le champ fautif, mais il est plus difficile à collecter. Il est collecté à l'exécution avec **OpenLineage**, par analyse statique du SQL, ou via des catalogues comme Marquez, DataHub ou Unity Catalog.

### Diapositive 14 — L'observabilité (≈ 1:00)

Le monitoring classique répond seulement à « le job a-t-il réussi ? ». L'**observabilité** répond à « pourquoi les données sont-elles fausses ou en retard ? ». Elle est **proactive** et s'appuie sur des métriques, des journaux structurés, des traces OpenTelemetry et des métadonnées de données.

On la résume en **cinq piliers** : fraîcheur, volume, schéma, distribution et lignage.

### Diapositive 15 — Scénario de diagnostic en 5 étapes (≈ 1:15)

Un exemple concret. **1. Détection** : une alerte signale -60 % de volume sur `sales_daily`. **2. Localisation** : le lignage montre que cette table dépend de `orders_clean`, elle-même alimentée par `orders_raw`. **3. Explication** : le job d'ingestion a réussi techniquement, mais n'a lu que 40 % des fichiers. **4. Cause racine** : une colonne a été renommée la veille en amont. **5. Impact** : le lignage aval liste trois tableaux de bord et un modèle de prévision touchés.

Résultat : la cause est trouvée en quelques minutes au lieu de plusieurs heures, ce qui réduit le MTTD et le MTTR.

En bas, la mise en œuvre avec Airflow (provider OpenLineage, Assets, métriques vers Prometheus et Grafana) et les limites : couverture incomplète, bruit d'alertes, et surtout **détecter n'est pas corriger**.

---

## Axe 4 — Compléter *(≈ 3:30)*

### Diapositive 16 — Limites des retries : principe et retry storm (≈ 1:15)

Un retry relance automatiquement une tâche échouée en espérant que la cause ait disparu. C'est efficace contre les **pannes transitoires** : coupure réseau brève, timeout ponctuel, service surchargé. Le délai suit la formule *min(délai_max, base × 2ⁿ) + aléa*.

Mais il y a des pièges. Le plus spectaculaire : la **tempête de relances**. Si chacune de trois couches successives tente trois fois, le service le plus bas peut recevoir **3 × 3 × 3 = 27 appels** pour une seule requête. Parades : jitter, limitation de débit, circuit breakers et retries limités à une seule couche.

### Diapositive 17 — Les 8 limites et leur parade (≈ 1:15)

Voici les huit limites, chacune avec sa parade.
1. **Erreur déterministe** : échoue à chaque fois, donc on classifie et on échoue immédiatement.
2. **Non-idempotence** : doublons, d'où `OVERWRITE`, `MERGE`, commit atomique.
3. **Retry storm** : jitter, circuit breaker.
4. **Panne durable** : alertes et escalade.
5. **Échec silencieux** : la tâche est verte mais les données sont fausses, d'où les quality gates bloquantes.
6. **Coût et latence** : checkpoints et tâches plus petites.
7. **Streaming** : doubles livraisons, donc sinks idempotents et déduplication.
8. **Pas de correction de fond** : dead-letter queue et rejeu après correction.

### Diapositive 18 — Mécanismes complémentaires (≈ 1:00)

Pour compléter le filet de sécurité : les **dead-letter queues** isolent les enregistrements toxiques sans bloquer le flux ; les **circuit breakers** suspendent les appels vers un service défaillant ; la **quarantaine** écarte les lots suspects ; le **backfill contrôlé** rejoue après correction ; et les **alertes SLA** déclenchent une escalade humaine quand la reprise automatique ne suffit pas.

---

## Conclusion *(≈ 1:30)*

### Diapositive 19 — Conclusion (≈ 1:00)

Pour résumer nos quatre questions : pour **récupérer**, on s'appuie sur l'état persisté, les retries et la reprise ciblée. Pour **prévenir**, des quality gates et des data contracts. Pour **diagnostiquer**, le lignage combiné à l'observabilité. Et pour **compléter**, l'idempotence, les dead-letter queues et les circuit breakers.

> [!warning] Phrase de clôture
> **Les retries sont un filet de sécurité, pas une stratégie de fiabilité.** La fiabilité en production repose sur la combinaison de tâches idempotentes, d'une reprise ciblée, de contrôles de qualité bloquants, d'un lignage et d'une observabilité qui permettent de diagnostiquer vite, et de stratégies de repli au-delà des retries.

### Diapositive 20 — Références (≈ 0:30)

Nos sources sont listées ici : documentation d'Airflow, d'OpenLineage, de Temporal et de Great Expectations, ainsi que des articles de recherche sur les RDD de Spark, Flink et la vérification de la qualité des données à grande échelle. Je vous remercie de votre attention, et nous sommes prêts à répondre à vos questions.

---

## Répartition suggérée (4 intervenants)

| Intervenant | Diapositives | Durée |
|---|---|---|
| 1 | 1 à 4 (introduction, contexte) | ≈ 4 min |
| 2 | 5 à 9 (axe 1 : récupérer) | ≈ 5 min |
| 3 | 10 à 15 (axes 2 et 3 : prévenir, diagnostiquer) | ≈ 7 min |
| 4 | 16 à 20 (axe 4 et conclusion) | ≈ 5 min |

## Questions probables du jury

> [!question] Préparez ces réponses
> - **Quelle différence entre monitoring et observabilité ?** Le monitoring donne un statut binaire (réussi ou échoué) de façon réactive ; l'observabilité suit en continu fraîcheur, volume, schéma et distribution, et explique le pourquoi, de façon proactive.
> - **Pourquoi l'idempotence est-elle indispensable ?** Parce que la reprise rejoue du code : sans idempotence, un retry après écriture partielle crée des doublons.
> - **Un retry suffit-il pour une erreur de code ?** Non : une erreur déterministe échoue à chaque tentative, il faut la classifier et échouer immédiatement.
> - **Lignage au niveau table ou colonne ?** Table : simple mais grossier. Colonne : précis pour la cause racine, mais plus difficile à collecter.
> - **Comment éviter une retry storm ?** Backoff exponentiel avec jitter, limitation de débit, circuit breakers, retries sur une seule couche.
