# tests/test_customer_sync_dag.py
import pytest
from airflow.models import DagBag
from datetime import datetime

class TestCustomerSyncDAG:
    """Integration tests for the full DAG"""

    @pytest.fixture
    def dagbag(self):
        """Load all DAGs"""
        return DagBag(dag_folder='dags/', include_examples=False)

    def test_dag_loaded(self, dagbag):
        """Test that DAG loads without errors"""
        dag = dagbag.get_dag(dag_id='customer_sync_with_contracts')
        assert dagbag.import_errors == {}
        assert dag is not None
        assert len(dag.tasks) == 6

    def test_dag_structure(self, dagbag):
        """Test DAG structure and dependencies"""
        dag = dagbag.get_dag(dag_id='customer_sync_with_contracts')

        # Check task dependencies
        extract_task = dag.get_task('extract_from_sql')
        validate_task = dag.get_task('validate_data_contract')
        quality_task = dag.get_task('apply_data_quality_checks')
        token_task = dag.get_task('get_api_token')
        send_task = dag.get_task('send_to_api')

        # Validate is downstream of extract
        assert validate_task in extract_task.downstream_list

        # Quality check is downstream of validate
        assert quality_task in validate_task.downstream_list

        # Send to API is downstream of quality check
        assert send_task in quality_task.downstream_list

        # Send to API is also downstream of get_api_token
        assert send_task in token_task.downstream_list

    def test_dag_default_args(self, dagbag):
        """Test DAG default arguments"""
        dag = dagbag.get_dag(dag_id='customer_sync_with_contracts')

        assert dag.default_args['owner'] == 'data_team'
        assert dag.default_args['retries'] == 2
        assert dag.default_args['start_date'] == datetime(2024, 1, 1)

    def test_dag_schedule(self, dagbag):
        """Test DAG schedule configuration"""
        dag = dagbag.get_dag(dag_id='customer_sync_with_contracts')

        assert dag.schedule_interval == '@daily'
        assert dag.catchup is False

    def test_all_tasks_present(self, dagbag):
        """Test that all expected tasks are present"""
        dag = dagbag.get_dag(dag_id='customer_sync_with_contracts')

        expected_tasks = [
            'extract_from_sql',
            'validate_data_contract',
            'apply_data_quality_checks',
            'get_api_token',
            'send_to_api'
        ]

        task_ids = [task.task_id for task in dag.tasks]

        for expected_task in expected_tasks:
            assert expected_task in task_ids