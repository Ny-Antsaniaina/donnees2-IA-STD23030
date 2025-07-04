from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys

# 🔧 Ajout du chemin absolu vers examen/scripts
dag_dir = os.path.dirname(__file__)
scripts_dir = os.path.abspath(os.path.join(dag_dir, "..", "scripts"))
sys.path.insert(0, scripts_dir)

# ✅ Import des fonctions une fois le chemin ajouté
from weather_etl import extract_weather_data, clean_weather_data, save_weather_data
from merge_weather_data import merge_weather_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 3),
    'retries': 1,
}

with DAG(
    dag_id="weather_etl_pipeline_examen",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags=["weather", "ETL"],
) as dag:

    extract = PythonOperator(
        task_id="extract_weather",
        python_callable=extract_weather_data
    )

    clean = PythonOperator(
        task_id="clean_weather",
        python_callable=clean_weather_data
    )

    save = PythonOperator(
        task_id="save_weather",
        python_callable=save_weather_data
    )

    merge = PythonOperator(
        task_id="merge_weather",
        python_callable=merge_weather_data
    )

    extract >> clean >> save >> merge
