from airflow.decorators import dag, task
from aiflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from datetime import datetime

@dag(
    schedule=None,
    start_date=datetime(2021, 1, 1),
    tags=['aws'],
)
def s3_sensor_example():

    wait_for_file = S3KeySensor(
        task_id='wait_for_file',
        aws_conn_id='aws_s3',
        bucket_key="s3://my-bucket/data_*",
        wildcard_match=True,
    )

    @task
    def process_file():
        print("File is available, processing it now...")
    
    wait_for_file >> process_file()

s3_sensor_dag = s3_sensor_example()