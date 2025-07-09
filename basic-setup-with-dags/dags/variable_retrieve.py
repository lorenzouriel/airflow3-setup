from airflow.sdk import dag, task, Variable

@dag
def variable_retrieve_dag():

    @task
    def print_variable():
        print(Variable.get("api", deserialize_json=True))

    print_variable()

variable_retrieve_dag()