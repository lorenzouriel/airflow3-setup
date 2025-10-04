from airflow import DAG
from airflow.decorators import task
from airflow.providers.http.hooks.http import SimpleHttpOperator

from datetime import datetime
import json

with DAG("sharing_dag", start_date=datetime(2025, 1, 1), schedule='@once'):

    get_api_resultas_task = SimpleHttpOperator(
        task_id="get_api",
        endpoints="/entries",
        do_xcom_push=True,
        http_conn_id="api",
        method="GET",
    )

    @task
    def parse_results(api_results):
        print(json.loads(api_results))

    parse_results(api_results=get_api_resultas_task.output)