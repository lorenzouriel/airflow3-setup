from airflow.decorators import task

@task.branch
def choose_path(execution_date=None):
    if execution_date.day == 1:
        return "monthly_task"
    return "daily_task"

monthly_task = EmptyOperator(task_id="monthly_task")
daily_task = EmptyOperator(task_id="daily_task")

choose_path() >> [monthly_task, daily_task]
