from airflow.sdk import dag, task, Context

@dag
def xcom_dag():
    @task
    def task_a(ti):
        values = {
            'task_a': 'Hello from push_xcom task A!',
            'task_c': 'Hello from push_xcom task C!'
        }
        ti.xcom_push(key='my_key', value=values)

    @task
    def task_b(ti):
        values = ti.xcom_pull(task_ids=['task_a', 'task_c'], key='my_key')
        print(f'Pulled values from XCom: {values}')

    task_a() >> task_b()

xcom_dag()  # Instantiate the DAG