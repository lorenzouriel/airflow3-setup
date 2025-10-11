from airflow.decorators import task, task_group
from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="taskgroup_decorator",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    @task
    def start():
        print("Start")

    @task_group(group_id="etl", tooltip="ETL Process")
    def etl_group():
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

    start() >> etl_group() >> end()
