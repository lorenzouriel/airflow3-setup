from airflow.decorators import task

@task.short_circuit
def has_data():
    # Skip downstream tasks if empty
    return True if get_data_count() > 0 else False

process_data = EmptyOperator(task_id="process_data")

has_data() >> process_data
