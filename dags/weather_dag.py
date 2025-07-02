from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

#  Ajout du chemin vers les scripts
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.abspath(os.path.join(current_dir, "..", "scripts"))
sys.path.append(scripts_dir)

#  Import des fonctions ETL
from weather_etl import extract_weather_data, clean_weather_data, save_weather_data
from merge_weather_data import merge_weather_data

#  Paramètres du DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 17),
    'retries': 1,
}

#  Définition du DAG principal
with DAG(
    dag_id='weather_etl_pipeline_examen',
    default_args=default_args,
    schedule='@daily',  # Exécution quotidienne
    catchup=False,
    max_active_runs=1,
    tags=["weather", "ETL"]
) as dag:

    # 1. Extraction des données météo
    extract = PythonOperator(
        task_id='extract_weather',
        python_callable=extract_weather_data,
    )

    # 2. Nettoyage des données extraites
    clean = PythonOperator(
        task_id='clean_weather',
        python_callable=clean_weather_data,
    )

    # 3. Sauvegarde des statistiques
    save = PythonOperator(
        task_id='save_weather',
        python_callable=save_weather_data,
    )

    # 4. Fusion avec données historiques
    merge = PythonOperator(
        task_id='merge_weather',
        python_callable=merge_weather_data,
    )

    # Dépendances du pipeline
    extract >> clean >> save >> merge
