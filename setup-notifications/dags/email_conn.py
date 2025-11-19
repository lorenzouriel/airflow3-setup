from airflow.utils.email import send_email_smtp
from airflow.decorators import dag, task
from datetime import datetime
import os

def gmail_fail_alert(context):
    ti = context["task_instance"]
    dag_id = ti.dag_id
    task_id = ti.task_id
    run_id = getattr(ti, "run_id", "unknown")
    execution_time = getattr(ti, "start_date", "unknown")
    error = str(context.get("exception", "No exception captured"))

    base_url = os.getenv("AIRFLOW__WEBSERVER__BASE_URL", "http://localhost:8080")
    log_url = f"{base_url}/dags/{dag_id}/runs/{run_id}"

    subject = f"🚨 Airflow Task Failed: {dag_id}.{task_id}"
    html_content = f"""
    <h3>🚨 Airflow Task Failed!</h3>
    <ul>
      <li><b>DAG:</b> {dag_id}</li>
      <li><b>Task:</b> {task_id}</li>
      <li><b>Run ID:</b> {run_id}</li>
      <li><b>Execution Time:</b> {execution_time}</li>
      <li><b>Error:</b> {error}</li>
    </ul>
    <p><a href="{log_url}">🔗 View Logs</a></p>
    """

    send_email_smtp(
        to="lorenzouriel394@gmail.com",
        subject=subject,
        html_content=html_content,
        conn_id="gmail_connection",  # your Airflow email connection ID
    )

@dag(
    dag_id="gmail_conn_alerts",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"on_failure_callback": gmail_fail_alert},
    tags=["alerts", "gmail"],
)
def gmail_notifier_dag():

    @task
    def failing_task():
        print("This task will fail 🚨")
        raise ValueError("Simulated failure for Gmail alert test")

    failing_task()

gmail_notifier_dag()