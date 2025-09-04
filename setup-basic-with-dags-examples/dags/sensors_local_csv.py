from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from datetime import datetime

@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    tags=['sensors'],
    catchup=False,
)
def local_csv_sensor_example():

    wait_for_files = FileSensor.partial(
        task_id='wait_for_files',
        fs_conn_id='fs_default',
    ).expand(
        filepath=['data_1.csv', 'data_2.csv', 'data_3.csv']
    )

    @task
    def process_files():
        print("All files are available, processing them now...")

    wait_for_files >> process_files()

local_csv_sensor_dag = local_csv_sensor_example()