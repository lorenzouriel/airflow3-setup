from airflow import DAG
from airflow.sensors.python import PythonSensor
import datetime

def _condition():
    return False

with DAG(
    dag_id="sensor",
    start_date=datetime(2021, 1, 1),
    schedule="@daily",
    catchup=False,
):
    waiting_for_condition = PythonSensor(
        task_id="waiting_for_condition",
        python_callable=_condition,
        mode="reschedule",  # Use reschedule mode to avoid blocking the worker
        poke_interval=60,  # Check every 10 seconds
        timeout=7 * 24 * 60 * 60,  # Timeout after 7 days
    )