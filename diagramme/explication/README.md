## 🗃️ Modèle de données : Modèle en étoile

Ce projet utilise un modèle en étoile avec une table de faits centrale et trois dimensions.

### Table de faits : `table_de_faits`
Contient les mesures météo journalières :

- `id_ville` (clé étrangère vers DIM_VILLE)
- `id_date` (clé étrangère vers DIM_DATE)
- `id_meteo` (clé étrangère vers DIM_METEO)
- `temp` : température moyenne du jour
- `humidity` : humidité moyenne

### Dimensions :

- **DIM_VILLE** : décrit les villes
  - `id_ville`, `nom_ville`, `pays`

- **DIM_DATE** : décrit le temps
  - `id_date`, `date`, `jour`, `mois`, `annee`

- **DIM_METEO** : type de météo
  - `id_meteo`, `description`, `is_rainy` (booléen)

Ce modèle permet une analyse efficace par ville, période ou météo.


