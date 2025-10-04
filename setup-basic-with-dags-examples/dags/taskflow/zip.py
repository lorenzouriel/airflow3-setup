from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator

from datetime import datetime

with DAG('dag', start_date=datetime(2022, 1, 1), schedule='@once', catchup=False):

    @task
    def get_path():
        return ['/usr/local/', '/bin/test/', '/home/me/']

    @task
    def get_filenames():
        return ['file_a', 'file_b', 'file_c']

    # get_filenames = PythonOperator(
    #     task_id='get_filenames',
    #     python_callable=lambda: ['file_a', 'file_b', 'file_c']
    # )

    @task
    def get_extensions():
        return ['.txt', '.zip', '.parquet']

    download = PythonOperator(
        task_id='download',
        python_callable=lambda file_a, file_b, file_c: print(f'{file_a} {file_b} {file_c}'),
        op_args=get_path().zip(get_filenames(), get_extensions())
    )

    
    # download = PythonOperator(
    #     task_id='download',
    #     python_callable=lambda file_a, file_b, file_c: print(f'{file_a} {file_b} {file_c}'),
    #     op_args=get_path().zip(get_filenames.output, get_extensions())
    # )