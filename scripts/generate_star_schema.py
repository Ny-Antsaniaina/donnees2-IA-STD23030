import pandas as pd
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
MERGED_FILE = os.path.join(DATA_DIR, "merge_weather_clean.csv")

def generate_star_schema():
    import traceback
    print("Génération du modèle en étoile...")
    try:
        if not os.path.exists(MERGED_FILE):
            raise FileNotFoundError("merge_weather_clean.csv introuvable")

        df = pd.read_csv(MERGED_FILE)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        villes = df["ville"].drop_duplicates().reset_index(drop=True)
        dim_ville = pd.DataFrame({
            "id_ville": range(1, len(villes)+1),
            "nom_ville": villes,
            "pays": villes.map({
                "Antananarivo": "MG",
                "Paris": "FR",
                "Tokyo": "JP",
                "London": "GB"
            })
        })
        dim_ville.to_csv(os.path.join(DATA_DIR, "DIM_VILLE.csv"), index=False)

        dates = df["date"].drop_duplicates().sort_values().reset_index(drop=True)
        dim_date = pd.DataFrame({
            "id_date": range(1, len(dates)+1),
            "date": dates,
            "jour": dates.dt.day,
            "mois": dates.dt.month,
            "annee": dates.dt.year
        })
        dim_date.to_csv(os.path.join(DATA_DIR, "DIM_DATE.csv"), index=False)

        dim_meteo = pd.DataFrame({
            "id_meteo": [0, 1],
            "description": ["No Rain", "Rain"],
            "is_rainy": [0, 1]
        })
        dim_meteo.to_csv(os.path.join(DATA_DIR, "DIM_METEO.csv"), index=False)

        df_fact = df.copy()
        df_fact = df_fact.merge(dim_ville, left_on="ville", right_on="nom_ville")
        df_fact = df_fact.merge(dim_date, on="date")
        df_fact["id_meteo"] = df_fact["is_rainy"]

        fact_table = df_fact[["id_ville", "id_date", "id_meteo", "temp", "humidity"]]
        fact_table.to_csv(os.path.join(DATA_DIR, "table_de_faits.csv"), index=False)
        print("Tables en étoile générées.")

    except Exception as e:
        print("ERREUR dans generate_star_schema:")
        print(traceback.format_exc())
        raise e
