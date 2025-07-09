from airflow.sdk import dag
from pendulum import datetime

@dag(
    schedule="@daily",
    start_date=datetime(2023, 10, 1),
    description="A simple DAG to demonstrate Airflow SDK usage",
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": 300,  # 5 minutes
    },
    catchup=False,
    tags=["first", "dag"],
    max_active_runs=1,
    max_consecutive_failed_dag_runs=3,
    concurrency=5,
)
def my_dag():
    pass

my_dag()