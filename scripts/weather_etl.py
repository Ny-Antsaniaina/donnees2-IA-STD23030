import os
import requests
import pandas as pd
from datetime import datetime

# 📁 Répertoire des données
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)

# 🔐 Lecture de la clé API depuis une variable d’environnement
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 🏙️ Liste des villes
VILLES = [
    {"nom": "Antananarivo", "pays": "MG"},
    {"nom": "Paris", "pays": "FR"},
    {"nom": "Tokyo", "pays": "JP"},
    {"nom": "London", "pays": "GB"},
]

def extract_weather_data():
    if not API_KEY:
        print("❌ ERREUR : clé API non trouvée dans les variables d’environnement.")
        return

    print("⏳ Début de l'extraction météo depuis OpenWeather...")
    all_data = []

    for ville in VILLES:
        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/forecast"
                f"?q={ville['nom']},{ville['pays']}&units=metric&appid={API_KEY}"
            )
            print(f"📡 Requête : {ville['nom']} → {url}")
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

            print(f"✅ Données récupérées pour {ville['nom']} : {len(data['list'])} points")

        except Exception as e:
            print(f"❌ Erreur pour {ville['nom']} : {e}")

    if all_data:
        df = pd.DataFrame(all_data)
        date_str = datetime.today().strftime("%Y-%m-%d")
        output_path = os.path.join(DATA_DIR, f"raw_weather_{date_str}.csv")
        df.to_csv(output_path, index=False)
        print(f"📁 Données enregistrées dans : {output_path}")
        print("👀 Aperçu :")
        print(df.head())
    else:
        print("⚠️ Aucun point météo collecté.")


def clean_weather_data():
    print("🧼 Nettoyage des données météo...")
    date_str = datetime.today().strftime("%Y-%m-%d")
    file_path = os.path.join(DATA_DIR, f"raw_weather_{date_str}.csv")

    if not os.path.exists(file_path):
        print(f"❌ Fichier introuvable : {file_path}")
        return

    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date", "temp", "weather"], inplace=True)

    df["is_rainy"] = df["weather"].apply(lambda w: 1 if "Rain" in w else 0)

    output_path = os.path.join(DATA_DIR, f"clean_weather_{date_str}.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Données nettoyées enregistrées dans : {output_path}")
    print(df.head())


def save_weather_data():
    print("📊 Calcul des statistiques journalières...")
    date_str = datetime.today().strftime("%Y-%m-%d")
    file_path = os.path.join(DATA_DIR, f"clean_weather_{date_str}.csv")

    if not os.path.exists(file_path):
        print(f"❌ Fichier introuvable : {file_path}")
        return

    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)
    df["day"] = df["date"].dt.date

    summary = df.groupby(["ville", "day"]).agg({
        "temp": "mean",
        "is_rainy": lambda x: 1 if x.sum() > 0 else 0
    }).reset_index()

    summary.columns = ["ville", "day", "temp", "is_rainy"]

    output_path = os.path.join(DATA_DIR, f"stats_weather_{date_str}.csv")
    summary.to_csv(output_path, index=False)
    print(f"✅ Statistiques sauvegardées dans : {output_path}")
    print(summary.head())
