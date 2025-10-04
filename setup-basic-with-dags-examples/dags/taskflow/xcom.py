from airflow import DAG
from airflow.decorators import task

from datetime import datetime


with DAG('sharing_dag', start_date=datetime(2022, 1 ,1), schedule='@once'):

   @task
   def t1():
       return 42

   @task(do_xcom_push=False)
   def t2(value: int) -> dict[str, int]:
       print(value)
       return {'my_val': 42, 'my_second_val': 56}

   @task
   def t3(first_value: int, second_value: int):
       print(first_value)
       print(second_value)


   values = t2(t1())
   t3(values['my_val'], values['my_second_val'])