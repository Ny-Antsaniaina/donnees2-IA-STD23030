import pandas as pd
from datetime import datetime
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)

def merge_weather_data():
    print(" Fusion des données météo...")

    try:
        date_str = datetime.today().strftime("%Y-%m-%d")

        hist_path = os.path.join(DATA_DIR, "openmeteo_hist_2020_2025.csv")
        recent_path = os.path.join(DATA_DIR, f"stats_weather_{date_str}.csv")
        output_path = os.path.join(DATA_DIR, "merge_weather.csv")

        df_hist = pd.read_csv(hist_path)
        df_recent = pd.read_csv(recent_path)

        df_hist["date"] = pd.to_datetime(df_hist["date"])
        df_recent = df_recent.rename(columns={"day": "date"})
        df_recent["date"] = pd.to_datetime(df_recent["date"])

        merged = pd.concat([df_hist, df_recent], ignore_index=True)
        merged.to_csv(output_path, index=False)

        print(f" Fusion terminée : {output_path}")
    except FileNotFoundError as e:
        print(f" Fichier manquant : {e.filename}")
    except Exception as e:
        print(f" Erreur : {e}")
