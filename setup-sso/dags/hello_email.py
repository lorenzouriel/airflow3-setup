from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="hello_world_alerts_email",
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False,
    default_args={
        "email": ["earthflow42@gmail.com", "lorenzouriel394@gmail.com"], 
        "email_on_failure": True,
        "email_on_retry": False,
    },
    tags=["hello!"],
)
def hello_world_dag():

    @task
    def say_hello():
        print("Hello World!")

        # Simulate failure
        raise ValueError("Simulated failure for testing alerts!")

    say_hello()

hello_world_dag()