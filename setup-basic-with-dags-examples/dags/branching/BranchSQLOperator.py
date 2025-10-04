from airflow.providers.common.sql.operators.sql import BranchSQLOperator
from airflow.operators.empty import EmptyOperator

branch = BranchSQLOperator(
    task_id="branch_sql",
    conn_id="my_postgres",
    sql="SELECT CASE WHEN COUNT(*) > 1000 THEN 'big_task' ELSE 'small_task' END FROM users;"
)

big_task = EmptyOperator(task_id="big_task")
small_task = EmptyOperator(task_id="small_task")

branch >> [big_task, small_task]
