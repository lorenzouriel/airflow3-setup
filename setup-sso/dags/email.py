from airflow.decorators import dag, task
from airflow.utils.email import send_email
from datetime import datetime

# To test email sending, run the following command in your terminal:
# docker exec -it setup-sso-airflow-apiserver-1 bash
# python -c "from airflow.utils.email import send_email; send_email('earthflow42@gmail.com', 'Test', 'This is a test')"

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

@dag(
    dag_id="email",
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False,
)
def hello_world_dag():

    @task(on_failure_callback=failure_email)
    def say_hello():
        print("Hello World!")
        raise ValueError("Simulated failure for testing alerts!")

    say_hello()

hello_world_dag()
