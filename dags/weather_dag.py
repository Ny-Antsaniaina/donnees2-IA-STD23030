from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys



#  Ajout du chemin absolu vers examen/scripts
dag_dir = os.path.dirname(__file__)
scripts_dir = os.path.abspath(os.path.join(dag_dir, "..", "scripts"))
sys.path.insert(0, scripts_dir)

# ✅ Import des fonctions une fois le chemin ajouté
from weather_etl import extract_weather_data, clean_weather_data, save_weather_data
from merge_weather_data import merge_weather_data
from get_5y_weather_openmeteo import download_all
from prepare_csv_for_looker import prepare_clean_csv
from generate_star_schema import generate_star_schema

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

    download_hist_weather_data = PythonOperator(
        task_id="download_hist_weather",
        python_callable=download_all
    )

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

    prepare_csv = PythonOperator(
        task_id="prepare_clean_csv",
        python_callable=prepare_clean_csv
    )

    generate_star = PythonOperator(
        task_id="generate_star_schema",
        python_callable=generate_star_schema
    )

    download_hist_weather_data >> extract >> clean >> save >> merge >> prepare_csv >> generate_star
