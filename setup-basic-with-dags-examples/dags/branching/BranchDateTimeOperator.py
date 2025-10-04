from airflow.operators.branch import BranchDateTimeOperator
from datetime import datetime, time

branch = BranchDateTimeOperator(
    task_id="branch_time",
    follow_task_ids_if_true="business_hours",
    follow_task_ids_if_false="off_hours",
    use_task_execution_date=True,
    start_date=datetime(2025,1,1,9,0),   # start 9AM
    end_date=datetime(2025,1,1,17,0),   # end 5PM
)

business_hours = EmptyOperator(task_id="business_hours")
off_hours = EmptyOperator(task_id="off_hours")

branch >> [business_hours, off_hours]
