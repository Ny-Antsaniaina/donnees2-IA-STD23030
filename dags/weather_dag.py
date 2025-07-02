from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.abspath(os.path.join(current_dir, "..", "scripts"))
sys.path.append(scripts_dir)

from weather_etl import extract_weather_data, clean_weather_data, save_weather_data
from merge_weather_data import merge_weather_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 17),
    'retries': 1,
}

with DAG(
    dag_id='weather_etl_pipeline_examen',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    max_active_runs=1,
    tags=["weather", "ETL"]
) as dag:

    extract = PythonOperator(
        task_id='extract_weather',
        python_callable=extract_weather_data,
    )

    clean = PythonOperator(
        task_id='clean_weather',
        python_callable=clean_weather_data,
    )

    save = PythonOperator(
        task_id='save_weather',
        python_callable=save_weather_data,
    )

    merge = PythonOperator(
        task_id='merge_weather',
        python_callable=merge_weather_data,
    )

    extract >> clean >> save >> merge
