import os
import requests
import pandas as pd
from datetime import datetime
from merge_weather_data import merge_weather_data

# Clé API OpenWeather
API_KEY = "8d4c33229d157905c817865855474725"

VILLES = [
    {"nom": "Antananarivo", "pays": "MG"},
    {"nom": "Paris", "pays": "FR"},
    {"nom": "Tokyo", "pays": "JP"},
    {"nom": "London", "pays": "GB"},
]

def extract_weather_data():
    print("Extraction des données météo...")
    all_data = []

    for ville in VILLES:
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={ville['nom']},{ville['pays']}&units=metric&appid={API_KEY}"
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()

            for item in data['list']:
                all_data.append({
                    "ville": ville["nom"],
                    "date": item["dt_txt"],
                    "temp": item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "weather": item["weather"][0]["main"]
                })
        except Exception as e:
            print(f"Erreur extraction {ville['nom']}: {e}")

    df = pd.DataFrame(all_data)
    os.makedirs("data", exist_ok=True)
    date_str = datetime.today().strftime("%Y-%m-%d")
    df.to_csv(f"data/raw_weather_{date_str}.csv", index=False)
    print("Extraction terminée.")


def clean_weather_data():
    print("Nettoyage des données météo...")
    date_str = datetime.today().strftime("%Y-%m-%d")
    df = pd.read_csv(f"data/raw_weather_{date_str}.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["is_rainy"] = df["weather"].apply(lambda w: 1 if "Rain" in w else 0)
    df.dropna(inplace=True)
    df.to_csv(f"data/clean_weather_{date_str}.csv", index=False)
    print("✅ Données nettoyées.")


def save_weather_data():
    print("Calcul des statistiques météo journalières...")
    date_str = datetime.today().strftime("%Y-%m-%d")
    df = pd.read_csv(f"data/clean_weather_{date_str}.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.date

    summary = df.groupby(["ville", "day"]).agg({
        "temp": "mean",
        "is_rainy": lambda x: 1 if x.sum() > 0 else 0
    }).reset_index()

    summary.columns = ["ville", "day", "temp", "is_rainy"]
    df_out_path = f"data/stats_weather_{date_str}.csv"
    summary.to_csv(df_out_path, index=False)
    print(f"Statistiques enregistrées dans {df_out_path}")


