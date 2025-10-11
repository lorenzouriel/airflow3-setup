from airflow import DAG
from airflow.decorators import task

from datetime import datetime
import random

with DAG(
    dag_id="expand_partial",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["example"],
) as dag:

    @task
    def get_files():
        return ["file_{nb}" for nb in range(random.randint(3, 5))]

    @task
    def download_files(folder: str, file: str):
        print(f"Downloading {file}")
    
    files = download_files.partial(folder='usr/local').expand(file=get_files())