# Standard library imports for path resolution
import sys
import os
# Ensure the parent directory is in the Python path so we can import custom modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Airflow decorators for defining tasks and DAGs
from airflow.decorators import task, dag

# Custom Python functions that load stock data
from include.stocks_daily import load_stock_daily
from include.stocks_historical import load_stock_historical

# # Used to define the DAG's start date
from datetime import datetime

# Define the DAG using the @dag decorator
@dag(
    dag_id="stocks_data_pipeline", # Unique identifier for this DAG
    description="Pipeline to run historical and daily stock data loading tasks",
    start_date=datetime(2025, 1, 1), # The first date this DAG is valid from
    schedule="0 0 * * *", # Cron schedule expression to run daily at midnight
    catchup=False # Prevents backfilling of previous runs when DAG is deployed
)

# Define the tasks within the DAG using the @task decorator
def stocks_data():
    """DAG for loading historical and daily stock data"""
    # Task to load historical stock data
    @task(task_id='load_stock_historical')
    def task_load_stock_historical():
        load_stock_historical() 
        return "Historical Data Loaded"

    # Task to load daily stock data
    @task(task_id='load_stock_daily')
    def task_load_stock_daily():
        load_stock_daily() 
        return "Daily Data Loaded"
    
    # Instantiate the tasks
    t1 = task_load_stock_historical()
    t2 = task_load_stock_daily()

    # Set task dependencies: historical must run before daily
    t1 >> t2

# Register the DAG in the Airflow scheduler
dag = stocks_data()