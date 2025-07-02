import pandas as pd
import os


def merge_weather_data():
    print(" Fusion des données historiques et récentes...")

    recent_path = "data/clean_weather.csv"
    hist_path = "data/open-meteo-35.70N139.69E40m.csv"
    output_path = "data/merge_weather.csv"

    # Vérification que les fichiers existent
    if not os.path.exists(hist_path) or not os.path.exists(recent_path):
        raise FileNotFoundError(" Fichier historique ou récent manquant.")

    # Chargement des données historiques (CSV brut Open-Meteo)
    df_hist = pd.read_csv(hist_path, skiprows=6)

    # Mapping location_id → nom de ville
    location_villes = {
        0: "Tokyo",
        1: "Antananarivo",
        2: "London",
        3: "Paris"
    }

    df_hist["ville"] = df_hist["location_id"].map(location_villes)

    # Renommage des colonnes pour uniformisation
    df_hist = df_hist.rename(columns={
        "time": "date",
        "temperature_2m (°C)": "temp",
        "rain (mm)": "is_rainy"
    })

    # Chargement des données récentes
    df_recent = pd.read_csv(recent_path)

    # Fusion des deux sources
    df_merge = pd.concat([
        df_hist[["ville", "date", "temp", "is_rainy"]],
        df_recent[["ville", "date", "temp", "is_rainy"]]
    ], ignore_index=True)

    # Nettoyage final
    df_merge.dropna(inplace=True)
    df_merge.drop_duplicates(subset=["ville", "date"], inplace=True)
    df_merge = df_merge.sort_values(by=["ville", "date"])

    # Sauvegarde
    df_merge.to_csv(output_path, index=False)
    print(" Fusion enregistrée dans merge_weather.csv")
