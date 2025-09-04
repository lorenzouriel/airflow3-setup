import requests
from airflow.decorators import dag, task
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

def task_fail_alert(context):
    ti = context["task_instance"]
    dag_id = ti.dag_id
    task_id = ti.task_id
    execution_time = getattr(ti, "start_date", "unknown")
    run_id = getattr(ti, "run_id", "unknown")
    try_number = getattr(ti, "try_number", "unknown")
    error = str(context.get("exception", "No exception captured"))

    # Optional: construct Airflow log URL if base is set
    base_url = os.getenv("AIRFLOW__WEBSERVER__BASE_URL", "http://localhost:8080")
    log_url = f"{base_url}/dags/{dag_id}/runs/{run_id}"

    message = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "🚨 **Airflow Task Failed!**",
                            "wrap": True,
                            "weight": "Bolder",
                            "color": "Attention",
                            "size": "Medium"
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {"title": "DAG", "value": dag_id},
                                {"title": "Task", "value": task_id},
                                {"title": "Run ID", "value": run_id},
                                {"title": "Execution Time", "value": str(execution_time)},
                                {"title": "Try", "value": str(try_number)},
                                {"title": "Error", "value": error}
                            ]
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "🔎 View Logs",
                            "url": log_url
                        }
                    ]
                }
            }
        ]
    }

    resp = requests.post(
        TEAMS_WEBHOOK_URL,
        json=message,
        headers={"Content-Type": "application/json"},
    )

    if resp.status_code in (200, 202):
        print("Teams alert sent successfully")
    else:
        print(f"Failed to send message to Teams: {resp.status_code} {resp.text}")


@dag(
    dag_id="teams",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"on_failure_callback": task_fail_alert},
    tags=["hello"],
)
def hello_world():

    @task
    def greet():
        print("Hello, World!")
        raise ValueError("Simulated failure for testing alerts!")

    greet()


hello_world()
