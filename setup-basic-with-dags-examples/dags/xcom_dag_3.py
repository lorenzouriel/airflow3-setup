from airflow.sdk import dag, task, Context

@dag
def xcom_dag():
    @task
    def push_xcom(ti):
        value = 'Hello from push_xcom!'
        ti.xcom_push(key='my_key', value=value)

    @task
    def pull_xcom(ti):
        ti.xcom_pull(task_ids='push_xcom', key='my_key')

    push_xcom() >> pull_xcom()

xcom_dag()  # Instantiate the DAG