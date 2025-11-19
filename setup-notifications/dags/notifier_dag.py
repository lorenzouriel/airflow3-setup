from airflow.decorators import dag, task
from datetime import datetime
from dags.notifier import failure_email, slack_fail_alert, task_fail_alert_teams

@dag(
    dag_id="example_alerts",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"on_failure_callback": slack_fail_alert},  # Can switch to email or Teams
)
def example_dag():
    @task(on_failure_callback=failure_email)  # Or task_fail_alert_teams
    def fail_task():
        print("This task will fail 🚨")
        raise ValueError("Simulated failure for testing alerts")

    fail_task()

example_dag()