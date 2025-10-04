from airflow import DAG
from airflow.decorators.python import PythonOperator

from datetime import datetime

with DAG("example_dag", start_date=datetime(2025, 1, 1), schedule='@once'):

    start = PythonOperator(
        task_id="start",
        python_callable=lambda: ['/usr/folder_a', '/usr/folder_b', '/usr/folder_c']
    )

    new_list = start.output.map(lambda path: path + 'data/')

    end = PythonOperator(
        task_id="end",
        python_callable=lambda new_list: print([path for path in new_list]),
        op_args=[new_list]
    )