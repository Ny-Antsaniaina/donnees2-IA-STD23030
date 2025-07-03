import os
import pandas as pd

def merge_weather_data():
    print(" Fusion des données historiques et récentes...")

    recent_path = "data/clean_weather.csv"
    hist_path = "data/openmeteo_hist_2020_2025.csv"
    output_path = "data/merge_weather.csv"

    # Vérification que les fichiers existent
    if not os.path.exists(hist_path) or not os.path.exists(recent_path):
        raise FileNotFoundError(" Fichier historique ou récent manquant.")

    # Chargement des données historiques (Open-Meteo déjà propre)
    df_hist = pd.read_csv(hist_path)

    # Renommage pour homogénéiser les noms avec les données récentes
    df_hist = df_hist.rename(columns={
        "date": "date",
        "temp": "temp",
        "is_rainy": "is_rainy",
    })

    # Chargement des données récentes
    df_recent = pd.read_csv(recent_path)

    # Sélection des colonnes utiles
    df_hist = df_hist[["ville", "date", "temp", "is_rainy"]]
    df_recent = df_recent[["ville", "date", "temp", "is_rainy"]]

    # Fusion
    df_merge = pd.concat([df_hist, df_recent], ignore_index=True)

    # Nettoyage final
    df_merge.dropna(inplace=True)
    df_merge.drop_duplicates(subset=["ville", "date"], inplace=True)
    df_merge = df_merge.sort_values(by=["ville", "date"])

    df_merge.to_csv(output_path, index=False)
    print("✅ Fusion enregistrée dans", output_path)
