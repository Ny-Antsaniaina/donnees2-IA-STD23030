import pandas as pd
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def prepare_clean_csv():
    print("🧹 Préparation du CSV final...")
    input_file = os.path.join(DATA_DIR, "merge_weather.csv")
    output_file = os.path.join(DATA_DIR, "merge_weather_clean.csv")

    if not os.path.exists(input_file):
        print(f"❌ Fichier non trouvé : {input_file}")
        return

    df = pd.read_csv(input_file)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["jour"] = df["date"].dt.day
    df["mois"] = df["date"].dt.month
    df["annee"] = df["date"].dt.year

    df_clean = df[["date", "jour", "mois", "annee", "ville", "temp", "is_rainy"]]
    df_clean.to_csv(output_file, index=False)
    print(f"✅ Données prêtes pour le dashboard : {output_file}")
