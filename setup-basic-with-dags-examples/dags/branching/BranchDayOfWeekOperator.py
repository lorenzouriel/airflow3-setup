from airflow.operators.branch import BranchDayOfWeekOperator

branch = BranchDayOfWeekOperator(
    task_id="branch_day",
    follow_task_ids_if_true="weekday_task",
    follow_task_ids_if_false="weekend_task",
    week_day=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
)

weekday_task = EmptyOperator(task_id="weekday_task")
weekend_task = EmptyOperator(task_id="weekend_task")

branch >> [weekday_task, weekend_task]
