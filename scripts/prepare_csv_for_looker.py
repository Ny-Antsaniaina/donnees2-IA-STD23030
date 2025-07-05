import pandas as pd
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def prepare_clean_csv():
    import traceback
    print("Préparation du fichier final clean pour dashboard...")
    try:
        input_file = os.path.join(DATA_DIR, "merge_weather.csv")
        output_file = os.path.join(DATA_DIR, "merge_weather_clean.csv")

        if not os.path.exists(input_file):
            raise FileNotFoundError("Fichier de fusion introuvable")

        df = pd.read_csv(input_file)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["jour"] = df["date"].dt.day
        df["mois"] = df["date"].dt.month
        df["annee"] = df["date"].dt.year

        df_clean = df[["date", "jour", "mois", "annee", "ville", "temp", "humidity", "is_rainy"]]
        df_clean.to_csv(output_file, index=False)
        print(f"Données prêtes pour le dashboard : {output_file}")

    except Exception as e:
        print("ERREUR dans prepare_clean_csv:")
        print(traceback.format_exc())
        raise e
