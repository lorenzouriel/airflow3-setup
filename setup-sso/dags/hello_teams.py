import requests
from airflow.decorators import dag, task
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')
TEAMS_WEBHOOK_URL = "https://defaultab65eb9cd51f43c8adb791dc0c21f7.72.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/5d88079648694aeabc9d674dc4009202/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=kAz31WBjR_pgeJpMs53B--y9jX156YD-CS-bPjQeN-k"


def task_fail_alert(context):
    dag_id = context.get("dag").dag_id
    task_id = context.get("task_instance").task_id
    execution_date = context.get("execution_date")
    log_url = context.get("task_instance").log_url

    message = (
        f"Airflow Task Failed!\n\n"
        f"DAG: {dag_id}\nTask: {task_id}\nExecution Date: {execution_date}\n"
        f"[View Logs]({log_url})"
    )

    requests.post(
        TEAMS_WEBHOOK_URL,
        json={"text": message},
        headers={"Content-Type": "application/json"}
    )

@dag(
    dag_id='hello_world_alerts_teams',
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False,
    default_args={
        "on_failure_callback": task_fail_alert,
    },
    tags=['hello'],
)
def hello_world():

    @task
    def greet():
        print("Hello, World!")

        # Simulate failure
        raise ValueError("Simulated failure for testing alerts!")

    greet()

hello_world()