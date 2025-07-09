from airflow.sdk import dag, task, Context

@dag
def xcom_dag():
    @task
    def push_xcom(**context: Context):
        context['ti'].xcom_push(key='my_key', value='Hello from push_xcom!')

    @task
    def pull_xcom(**context: Context):
        value = context['ti'].xcom_pull(task_ids='push_xcom', key='my_key')
        print(f'Pulled value from XCom: {value}')

    push_task = push_xcom()
    pull_task = pull_xcom()

    push_task >> pull_task

xcom_dag()  # Instantiate the DAG