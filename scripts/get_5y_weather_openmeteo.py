# scripts/get_5y_weather_openmeteo.py

from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)

#  Coordonnées GPS des villes
VILLES = {
    "Antananarivo": (-18.8792, 47.5079),
    "Paris": (48.8566, 2.3522),
    "Tokyo": (35.6895, 139.6917),
    "London": (51.5074, -0.1278)
}

# Calcul des dates
TODAY = datetime.now().date()
START_DATE = (datetime.now() - relativedelta(years=5)).date()
YEARS_RANGE = f"{START_DATE.year}_{TODAY.year}"
OUTPUT_FILE = os.path.join(DATA_DIR, f"openmeteo_hist_{YEARS_RANGE}.csv")

def get_openmeteo_data(lat, lon, ville):
    print(f" Téléchargement des données pour {ville}...")
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={START_DATE}&end_date={TODAY}"
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data["daily"])
        df["ville"] = ville
        return df
    except Exception as e:
        print(f" Erreur pour {ville}: {e}")
        return pd.DataFrame()

def download_all():
    print(" Démarrage de la collecte historique sur 5 ans...\n")
    dfs = []

    for ville, (lat, lon) in VILLES.items():
        df = get_openmeteo_data(lat, lon, ville)
        if not df.empty:
            dfs.append(df)

    if dfs:
        df_total = pd.concat(dfs)

        df_total = df_total.rename(columns={
            "time": "date",
            "temperature_2m_mean": "temp",
            "precipitation_sum": "is_rainy"
        })

        df_total["is_rainy"] = df_total["is_rainy"].apply(lambda x: 1 if x > 0 else 0)

        df_total.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✅ Données enregistrées dans: {OUTPUT_FILE}")
    else:
        print(" Aucune donnée téléchargée.")


