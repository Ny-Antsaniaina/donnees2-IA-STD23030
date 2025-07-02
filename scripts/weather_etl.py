import os
import requests
import pandas as pd
from datetime import datetime

API_KEY = "8d4c33229d157905c817865855474725"

villes = [
    {"nom": "Antananarivo", "pays": "MG"},
    {"nom": "Paris", "pays": "FR"},
    {"nom": "Tokyo", "pays": "JP"},
    {"nom": "London", "pays": "GB"}
]

def extract_weather_data():
    print(" Extraction des données météo...")
    all_data = []

    for ville in villes:
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={ville['nom']},{ville['pays']}&units=metric&appid={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data['list']:
                all_data.append({
                    "ville": ville['nom'],
                    "date": item['dt_txt'],
                    "temp": item['main']['temp'],
                    "humidity": item['main']['humidity'],
                    "weather": item['weather'][0]['main']
                })

        except Exception as e:
            print(f"❌ Erreur API pour {ville['nom']}: {e}")

    df = pd.DataFrame(all_data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_weather.csv", index=False)
    print("✅ Extraction terminée.")

def clean_weather_data():
    print(" Nettoyage des données météo...")
    df = pd.read_csv("data/raw_weather.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["is_rainy"] = df["weather"].apply(lambda w: 1 if "Rain" in w else 0)
    df.dropna(inplace=True)
    df.to_csv("data/clean_weather.csv", index=False)
    print(" Données nettoyées et sauvegardées.")

def save_weather_data():
    print(" Sauvegarde des statistiques météo...")
    df = pd.read_csv("data/clean_weather.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.date

    summary = df.groupby(["ville", "day"]).agg({
        "temp": "mean",
        "is_rainy": lambda x: 1 if x.sum() > 0 else 0
    }).reset_index()

    summary.columns = ["ville", "day", "temp_moyenne", "jour_pluvieux"]
    summary.to_csv("data/stats_weather.csv", index=False)
    print("✅ Statistiques météo enregistrées.")
