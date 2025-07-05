import os
import pandas as pd
from datetime import datetime

import requests

from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv(f"OPENWEATHER_API_KEY")

VILLES = [
    {"nom": "Antananarivo", "pays": "MG"},
    {"nom": "Paris", "pays": "FR"},
    {"nom": "Tokyo", "pays": "JP"},
    {"nom": "London", "pays": "GB"},
]

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)


def extract_weather_data():
    import traceback
    print("Extraction des données OpenWeather...")
    try:
        if not API_KEY:
            raise ValueError("Clé API manquante !")

        all_data = []

        for ville in VILLES:
            url = (
                f"https://api.openweathermap.org/data/2.5/forecast"
                f"?q={ville['nom']},{ville['pays']}&units=metric&appid={API_KEY}"
            )
            print(f"Requête : {url}")
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

        if not all_data:
            raise ValueError("Aucune donnée collectée")

        df = pd.DataFrame(all_data)
        output_path = os.path.join(DATA_DIR, f"raw_weather_{datetime.today().strftime('%Y-%m-%d')}.csv")
        df.to_csv(output_path, index=False)
        print(f"Données extraites : {output_path}")

    except Exception as e:
        print("ERREUR dans extract_weather_data:")
        print(traceback.format_exc())
        raise e


def clean_weather_data():
    import traceback
    print("Nettoyage des données météo...")
    try:
        date_str = datetime.today().strftime("%Y-%m-%d")
        file_path = os.path.join(DATA_DIR, f"raw_weather_{date_str}.csv")

        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df.dropna(subset=["date", "temp", "weather", "humidity"], inplace=True)
        df["is_rainy"] = df["weather"].apply(lambda w: 1 if "Rain" in w else 0)

        output_path = os.path.join(DATA_DIR, f"clean_weather_{date_str}.csv")
        df.to_csv(output_path, index=False)
        print(f"Données nettoyées : {output_path}")

    except Exception as e:
        print("ERREUR dans clean_weather_data:")
        print(traceback.format_exc())
        raise e


def save_weather_data():
    import traceback
    print("Calcul des stats journalières météo...")
    try:
        date_str = datetime.today().strftime("%Y-%m-%d")
        file_path = os.path.join(DATA_DIR, f"clean_weather_{date_str}.csv")

        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df.dropna(subset=["date"], inplace=True)
        df["day"] = df["date"].dt.date

        summary = df.groupby(["ville", "day"]).agg({
            "temp": "mean",
            "humidity": "mean",
            "is_rainy": lambda x: 1 if x.sum() > 0 else 0
        }).reset_index()

        summary.columns = ["ville", "day", "temp", "humidity", "is_rainy"]
        output_path = os.path.join(DATA_DIR, f"stats_weather_{date_str}.csv")
        summary.to_csv(output_path, index=False)
        print(f"Données sauvegardées : {output_path}")

    except Exception as e:
        print("ERREUR dans save_weather_data:")
        print(traceback.format_exc())
        raise e
