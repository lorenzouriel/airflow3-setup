from airflow.sdk import dag, task, chain
from pendulum import datetime

@dag(
    schedule="@daily",
    start_date=datetime(2023, 10, 1),
    description="A simple DAG to demonstrate Airflow SDK usage",
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": 300,  # 5 minutes
    },
    catchup=False,
    tags=["first", "dag"],
    max_active_runs=1,
    max_consecutive_failed_dag_runs=3,
    concurrency=5,
)
def my_dag():
    
    @task
    def task_a():
        print("Hello, Task A!")

    @task
    def task_b():
        print("Hello, Task B!")

    @task
    def task_c():
        print("Hello, Task C!")

    @task
    def task_d():
        print("Hello, Task D!")

    @task
    def task_e():
        print("Hello, Task E!")

    # Define task dependencies

    # Upstream tasks can be defined using the >> operator
        # task_a() >> task_b() >> task_c() >> task_d()
    # or the << operator for downstream tasks.
        # task_a() << task_b() << task_c() << task_d()

    # Alternatively, you can use lists to define multiple downstream tasks
        # task_a() >> [task_b(), task_c()] 

    # To create a list of dependencies
        # task_a() >> task_b >> [task_c(), task_d()] 

    # To create a more complex dependency graph
    chain(task_a(), [task_b(), task_d()], [task_c(), task_e()])

my_dag() # Instantiate the DAG