# notifier.py
import os
import logging
import requests
from airflow.utils.email import send_email
from airflow.models import Variable
from dotenv import load_dotenv

load_dotenv()

# ------------------------------
# Email Notifier
# ------------------------------
def failure_email(context):
    ti = context['task_instance']
    execution_date = getattr(ti, "start_date", "Unknown")
    log_url = getattr(ti, "log_url", "#")
    subject = f"Task {ti.task_id} failed"
    body = f"""
    DAG: {ti.dag_id} <br>
    Task: {ti.task_id} <br>
    Execution Time: {execution_date} <br>
    <a href='{log_url}'>Logs</a>
    """
    send_email(to=["earth@gmail.com"], subject=subject, html_content=body)
    logging.info(f"Failure email sent for task {ti.task_id} in DAG {ti.dag_id}")


# ------------------------------
# Teams Notifier
# ------------------------------
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

def task_fail_alert_teams(context):
    ti = context["task_instance"]
    dag_id = ti.dag_id
    task_id = ti.task_id
    execution_time = getattr(ti, "start_date", "unknown")
    run_id = getattr(ti, "run_id", "unknown")
    try_number = getattr(ti, "try_number", "unknown")
    error = str(context.get("exception", "No exception captured"))

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
                        {"type": "TextBlock",
                         "text": "🚨 **Airflow Task Failed!**",
                         "wrap": True, "weight": "Bolder", "color": "Attention", "size": "Medium"},
                        {"type": "FactSet", "facts": [
                            {"title": "DAG", "value": dag_id},
                            {"title": "Task", "value": task_id},
                            {"title": "Run ID", "value": run_id},
                            {"title": "Execution Time", "value": str(execution_time)},
                            {"title": "Try", "value": str(try_number)},
                            {"title": "Error", "value": error}
                        ]}
                    ],
                    "actions": [{"type": "Action.OpenUrl", "title": "🔎 View Logs", "url": log_url}]
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
        logging.info("Teams alert sent successfully")
    else:
        logging.error(f"Failed to send Teams message: {resp.status_code} {resp.text}")


# ------------------------------
# Slack Notifier
# ------------------------------
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
            {"type": "section", "text": {"type": "mrkdwn", "text": ":rotating_light: *Airflow Task Failed!*"}},
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
