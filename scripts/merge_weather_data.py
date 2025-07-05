import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def merge_weather_data():
    import traceback
    print("🔗 Fusion des fichiers météo...")
    try:
        date_str = datetime.today().strftime("%Y-%m-%d")
        start = datetime.now() - relativedelta(years=5)
        years_range = f"{start.year}_{datetime.now().year}"

        hist_path = os.path.join(DATA_DIR, f"openmeteo_hist_{years_range}.csv")
        recent_path = os.path.join(DATA_DIR, f"stats_weather_{date_str}.csv")
        output_path = os.path.join(DATA_DIR, "merge_weather.csv")

        if not os.path.exists(hist_path) or not os.path.exists(recent_path):
            raise FileNotFoundError("Fichier historique ou récent manquant")

        df_hist = pd.read_csv(hist_path)
        df_recent = pd.read_csv(recent_path)

        df_hist["date"] = pd.to_datetime(df_hist["date"], errors="coerce")
        df_recent = df_recent.rename(columns={"day": "date"})
        df_recent["date"] = pd.to_datetime(df_recent["date"], errors="coerce")

        merged = pd.concat([df_hist, df_recent], ignore_index=True)
        merged.to_csv(output_path, index=False)
        print(f"✅ Fichier fusionné : {output_path}")

    except Exception as e:
        print("❌ ERREUR dans merge_weather_data:")
        print(traceback.format_exc())
        raise e
