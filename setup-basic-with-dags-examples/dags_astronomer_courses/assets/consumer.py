from airflow.sdk import asset
from include import a

@asset(schedule=a)
def b():
    pass