import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from airflow.decorators import task, dag
from include.stocks_daily import load_stock_daily
from include.stocks_historical import load_stock_historical
from datetime import datetime

@dag(
    dag_id="stocks-daily",
    description="Pipeline to run historical and daily stock data loading tasks",
    start_date=datetime(2025, 1, 10),
    schedule="0 0 * * *",  # ✅ corrigido
    catchup=False
)
def stocks_data():

    @task(task_id='load_stock_historical')
    def task_load_stock_historical():
        load_stock_historical() 
        return "Historical Data Loaded"

    @task(task_id='load_stock_daily')
    def task_load_stock_daily():
        load_stock_daily() 
        return "Daily Data Loaded"
    
    t1 = task_load_stock_historical()
    t2 = task_load_stock_daily()

    t1 >> t2  

stocks_data()