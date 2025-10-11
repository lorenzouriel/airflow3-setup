from airflow.operators.python import BranchExternalPythonOperator

def check_dependencies():
    try:
        import tensorflow
        return "ml_task"
    except ImportError:
        return "fallback_task"

branch = BranchExternalPythonOperator(
    task_id="branch_external",
    python="/usr/bin/python3.9",
    python_callable=check_dependencies
)

ml_task = EmptyOperator(task_id="ml_task")
fallback_task = EmptyOperator(task_id="fallback_task")

branch >> [ml_task, fallback_task]
