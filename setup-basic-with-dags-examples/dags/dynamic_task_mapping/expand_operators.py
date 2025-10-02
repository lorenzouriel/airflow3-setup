from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

from datetime import datetime
import random

with DAG(
    dag_id="expand_partial_with_operators",
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
        return f"ls {folder}/{file}; exit 0"
    
    files = download_files.partial(folder='usr/local').expand(file=get_files())

    BashOperator.partial(task_id="ls file").expand(bash_command=files)