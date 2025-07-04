import pandas as pd
from datetime import datetime
import os

def merge_weather_data():
    print("📦 Démarrage de la fusion des données météo...")

    try:
        # 📅 Date du jour au format YYYY-MM-DD
        date_str = datetime.today().strftime("%Y-%m-%d")

        # 📁 Chemins vers les fichiers
        hist_path = "data/openmeteo_hist_2020_2025.csv"
        recent_path = f"data/stats_weather_{date_str}.csv"

        print(f"🔍 Lecture de : {hist_path}")
        print(f"🔍 Lecture de : {recent_path}")

        # 📄 Chargement des données
        df_hist = pd.read_csv(hist_path)
        df_recent = pd.read_csv(recent_path)

        print(f"✅ Historique chargé : {df_hist.shape[0]} lignes")
        print(f"✅ Récent chargé : {df_recent.shape[0]} lignes")

        # 📅 Harmonisation des noms de colonnes et des types
        df_hist["date"] = pd.to_datetime(df_hist["date"])
        df_recent = df_recent.rename(columns={"day": "date"})
        df_recent["date"] = pd.to_datetime(df_recent["date"])

        # 🔄 Fusion
        merged = pd.concat([df_hist, df_recent], ignore_index=True)

        # 💾 Sauvegarde
        os.makedirs("data", exist_ok=True)
        merged.to_csv("data/merge_weather.csv", index=False)

        print("✅ Fusion terminée et enregistrée dans : data/merge_weather.csv")

    except FileNotFoundError as e:
        print(f"❌ Fichier manquant : {e.filename}")
    except Exception as e:
        print(f"❌ Erreur inattendue lors de la fusion : {e}")
