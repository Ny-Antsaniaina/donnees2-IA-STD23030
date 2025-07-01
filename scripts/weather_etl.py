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
    all_data = []
    for ville in villes:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={ville['nom']},{ville['pays']}&units=metric&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Erreur API pour {ville['nom']} : {response.status_code}")
            continue
        data = response.json()
        for item in data['list']:
            all_data.append({
                "ville": ville['nom'],
                "date": item['dt_txt'],
                "temp": item['main']['temp'],
                "humidity": item['main']['humidity'],
                "weather": item['weather'][0]['main']
            })
    df = pd.DataFrame(all_data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_weather.csv", index=False)

def clean_weather_data():
    df = pd.read_csv("data/raw_weather.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["is_rainy"] = df["weather"].apply(lambda w: 1 if "Rain" in w else 0)
    df.dropna(inplace=True)
    df.to_csv("data/clean_weather.csv", index=False)

def save_weather_data():
    df = pd.read_csv("data/clean_weather.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.date
    summary = df.groupby(["ville", "day"]).agg({
        "temp": "mean",
        "is_rainy": "sum"
    }).reset_index()
    summary.columns = ["ville", "day", "temp_moyenne", "nb_jours_pluvieux"]
    summary.to_csv("data/stats_weather.csv", index=False)
