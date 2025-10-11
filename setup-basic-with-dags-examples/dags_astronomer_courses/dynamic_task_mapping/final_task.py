from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

from datetime import datetime
import random

with DAG(dag_id='final_task', start_date=datetime(2022, 1, 1), schedule_interval='@daily', catchup=False) as dag:

   @task
   def get_files():
       return [f"file_{nb}" for nb in range(random.randint(3, 5))]

   @task
   def download_file(folder: str, file: str):
       return f"{folder}/{file}"


   files = download_file.partial(folder='/usr/local').expand(file=get_files())

   print_files = BashOperator(task_id='print_files', bash_command="echo '{{ ti.xcom_pull(task_ids='download_file', dag_id='my_dag', key='return_value') | list }}'")

   files >> print_files