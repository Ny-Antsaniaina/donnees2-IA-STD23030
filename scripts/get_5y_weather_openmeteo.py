import requests
import pandas as pd
import os

#  Dossier de sortie
os.makedirs("data", exist_ok=True)

#  Coordonnées GPS de chaque ville
villes = {
    "Antananarivo": (-18.8792, 47.5079),
    "Paris": (48.8566, 2.3522),
    "Tokyo": (35.6895, 139.6917),
    "London": (51.5074, -0.1278)
}

def get_openmeteo_data(lat, lon, ville):
    print(f" Téléchargement des données pour {ville}...")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date=2020-01-01&end_date=2025-07-03"
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data['daily'])
        df['ville'] = ville
        return df
    except Exception as e:
        print(f"❌ Erreur pour {ville} : {e}")
        return pd.DataFrame()

#  Récupération pour toutes les villes
dfs = []
for ville, (lat, lon) in villes.items():
    df = get_openmeteo_data(lat, lon, ville)
    if not df.empty:
        dfs.append(df)

#  Fusion et sauvegarde
if dfs:
    df_total = pd.concat(dfs)
    df_total = df_total.rename(columns={
        "time": "date",
        "temperature_2m_mean": "temp",
        "precipitation_sum": "is_rainy"
    })

    # Binaire : pluie ou pas (0 mm = pas de pluie)
    df_total["is_rainy"] = df_total["is_rainy"].apply(lambda x: 1 if x > 0 else 0)

    df_total.to_csv("data/openmeteo_hist_2020_2025.csv", index=False)
    print("✅ Données enregistrées dans data/openmeteo_hist_2020_2025.csv")
else:
    print(" Aucune donnée téléchargée.")
