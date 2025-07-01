import sys
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.merge_weather_data import merge_weather_data
from scripts.weather_etl import extract_weather_data, clean_weather_data, save_weather_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))



default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 17),
    'retries': 1
}

with DAG(
    dag_id='weather_etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
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
