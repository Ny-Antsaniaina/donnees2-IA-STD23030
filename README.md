# 🌦️ Projet Météo — Comparaison climatique entre villes du monde

## 👤 Auteur
- **Nom** : Ny Antsaniaina Fanomezantsoa RAHARIMBOAVONJY
- **Email** : hei.nyantsaniaina@gmail.com

---

## 🎯 Objectif du projet

Ce projet vise à comparer l’évolution du climat dans plusieurs grandes villes (Antananarivo, Paris, Tokyo, Londres) à l’aide d’un pipeline ETL automatisé, de données météorologiques historiques et récentes, et d’une visualisation interactive.

### Problématique :
> Comment évolue le climat dans plusieurs grandes villes ? Peut-on classer les villes selon leur stabilité ou leur extrémisme climatique ?

---

## 🔁 Pipeline ETL automatisé avec Airflow

Un DAG Airflow orchestre les différentes étapes de collecte, traitement et fusion des données météo.

### `weather_etl_pipeline_examen.py` :

1. `download_hist_weather` → Données historiques OpenMeteo (5 ans)
2. `extract_weather` → Données récentes OpenWeather (prévisions)
3. `clean_weather` → Nettoyage et ajout de la colonne `is_rainy`
4. `save_weather` → Moyenne quotidienne par ville
5. `merge_weather` → Fusion historique + prévisions
6. `prepare_clean_csv` → Nettoyage final pour dashboard

📁 **Données fusionnées disponibles** : `merge_weather_clean.csv`

---

## 🗃️ Modèle de données : Modèle en étoile

Le modèle en étoile est composé d’une table de faits centrale et de trois dimensions : Ville, Date, Météo.

### ✅ Table de faits : `table_de_faits`

Contient les mesures météo observées chaque jour dans chaque ville :
- `id_ville` (clé étrangère vers DIM_VILLE)
- `id_date` (clé étrangère vers DIM_DATE)
- `id_meteo` (clé étrangère vers DIM_METEO)
- `temp` : température moyenne (°C)
- `humidity` : humidité (%)

### ✅ Dimensions :
- **DIM_VILLE** : `id_ville`, `nom_ville`, `pays`
- **DIM_DATE** : `id_date`, `date`, `jour`, `mois`, `annee`
- **DIM_METEO** : `id_meteo`, `description`, `is_rainy` (0 ou 1)

📎 **Diagramme du modèle** :

![Diagramme Étoile](../examen/diagramme/image/diagramme_etoile.png)

---

## 📊 Analyse exploratoire (EDA)

Réalisée dans le notebook : `EDA_weather.ipynb`

### 🔍 Indicateurs analysés :
- Température moyenne par ville
- Nombre de jours pluvieux
- Score météo extrême (écart-type + amplitude + pluie)
- Corrélation pluie/température (scatter plot)

### 📈 Résultats :
| Ville        | Température Moyenne | Jours Pluvieux | Score Extrême |
|--------------|----------------------|----------------|----------------|
| Tokyo        | 15.2°C               | 470 jours      | 55.87          |
| Paris        | 12.9°C               | 390 jours      | 46.10          |
| London       | 11.8°C               | 460 jours      | 51.43          |
| Antananarivo | 18.4°C               | 230 jours      | 31.06          |

✅ **Ville la plus extrême** : **London**  
✅ **Ville la plus stable** : **Tokyo**

---

## 📈 Dashboard interactif

🔗 [Lien Looker Studio](https://lookerstudio.google.com/reporting/5c00cc9c-d6d6-4bea-87fc-447feacb750a) 

### Fonctionnalités :
- Filtres dynamiques : ville, mois, année
- Visualisation des températures et jours de pluie
- Comparaison des villes
- Évolution temporelle interactive

---

## ⚙️ Technologies utilisées

| Composant      | Outil                    |
|----------------|--------------------------|
| Extraction     | Python (Requests, API)   |
| Traitement     | Pandas                   |
| Automatisation | Apache Airflow           |
| Visualisation  | Matplotlib, Seaborn, Looker Studio |
| Stockage       | Fichiers CSV             |

---

## 🗃️ Fichiers livrables

| Fichier                           | Description                            |
|----------------------------------|----------------------------------------|
| `weather_etl_pipeline_examen.py` | DAG Airflow                            |
| `merge_weather_clean.csv`        | Données finales nettoyées              |
| `EDA_weather.ipynb`              | Analyse exploratoire                   |
| `diagramme_etoile.png`           | Modèle de données (image)              |
| `README.md`                      | Documentation complète                 |

---

## 🧠 Conclusion

Ce projet démontre qu’un pipeline automatisé peut collecter, nettoyer, et analyser efficacement des données météo, permettant de classer des villes selon des critères de stabilité ou d’extrême climatique.  
L’ajout d’un dashboard interactif permet une exploration simple et intuitive par tout utilisateur.

