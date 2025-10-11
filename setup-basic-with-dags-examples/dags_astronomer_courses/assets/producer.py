from airflow.sdk import asset

@asset(schedule="@daily", uri="s3://my-bucket/data/producer/")
def producer():
    pass