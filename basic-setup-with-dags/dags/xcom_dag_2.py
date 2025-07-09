from airflow.sdk import dag, task, Context

@dag
def xcom_dag():
    @task
    def push_xcom():
        value = 'Hello from push_xcom!'
        return value

    @task
    def pull_xcom(value: str):
        print(value)

    value = push_xcom()
    pull_xcom(value)

xcom_dag()  # Instantiate the DAG