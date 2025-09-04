import requests
import logging
from airflow.decorators import dag, task
from airflow.models import Variable
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def slack_fail_alert(context):
    ti = context["task_instance"]
    dag_id = ti.dag_id
    task_id = ti.task_id
    run_id = getattr(ti, "run_id", "unknown")
    try_number = getattr(ti, "try_number", "unknown")
    execution_time = getattr(ti, "start_date", "unknown")
    error = str(context.get("exception", "No exception captured"))
    log_url = getattr(ti, "log_url", "N/A")

    message = {
        "text": f":rotating_light: *Airflow Task Failed!*",
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f":rotating_light: *Airflow Task Failed!*"}},
            {"type": "section", "fields": [
                {"type": "mrkdwn", "text": f"*DAG:*\n{dag_id}"},
                {"type": "mrkdwn", "text": f"*Task:*\n{task_id}"},
                {"type": "mrkdwn", "text": f"*Run ID:*\n{run_id}"},
                {"type": "mrkdwn", "text": f"*Try:*\n{try_number}"},
                {"type": "mrkdwn", "text": f"*Execution Time:*\n{execution_time}"},
                {"type": "mrkdwn", "text": f"*Error:*\n{error}"}
            ]},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"<{log_url}|View Logs>"}}
        ]
    }

    slack_url = Variable.get("slack_webhook_url", default_var=SLACK_WEBHOOK_URL)

    logging.info(f"Sending Slack notification: {message}")
    response = requests.post(slack_url, json=message)

    if response.status_code not in (200, 201):
        logging.error(f"Failed to send Slack notification: {response.status_code} {response.text}")
    else:
        logging.info("Slack notification sent successfully")

@dag(
    dag_id="slack",
    start_date=datetime(2025, 1, 5),
    schedule=None,
    catchup=False,
    default_args={"on_failure_callback": slack_fail_alert},  # DAG-level callback
)
def slack_notifier_dag():

    @task
    def failing_task():
        print("This task will fail 🚨")
        raise ValueError("Simulated failure for Slack alert test")

    failing_task()

slack_notifier_dag()