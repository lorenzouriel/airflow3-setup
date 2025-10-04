from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from datetime import datetime

with DAG(
    dag_id="taskgroup_classic",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    @task
    def start():
        print("Start")

    with TaskGroup("etl", tooltip="ETL Process") as etl_group:
        @task
        def extract():
            print("Extract")

        @task
        def transform():
            print("Transform")

        @task
        def load():
            print("Load")

        extract() >> transform() >> load()

    @task
    def end():
        print("End")

    start() >> etl_group >> end()
