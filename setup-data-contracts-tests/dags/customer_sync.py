from airflow import DAG
from airflow.decorators import task
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from datetime import datetime
import pandas as pd
import requests
from typing import Dict, List
from pydantic import BaseModel, ValidationError, Field, validator
import great_expectations as ge

# Define your data contract using Pydantic
class CustomerRecord(BaseModel):
    """Data contract for customer records from SQL Server"""
    customer_id: int = Field(..., gt=0)
    email: str
    name: str = Field(..., min_length=1, max_length=100)
    created_date: datetime
    total_purchases: float = Field(..., ge=0)
    status: str
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['active', 'inactive', 'suspended']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of {allowed_statuses}')
        return v

class APIPayload(BaseModel):
    """Data contract for API payload"""
    customers: List[Dict]
    batch_id: str
    timestamp: datetime
    record_count: int

default_args = {
    'owner': 'data_team',
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
}

with DAG(
    'customer_sync_with_contracts',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    @task
    def extract_from_sql() -> List[Dict]:
        """Extract data from SQL Server with basic validation"""
        hook = MsSqlHook(mssql_conn_id='sql_server_conn')
        
        query = """
        SELECT 
            customer_id,
            email,
            name,
            created_date,
            total_purchases,
            status
        FROM customers
        WHERE updated_date >= DATEADD(day, -1, GETDATE())
        """
        
        df = hook.get_pandas_df(query)
        
        # Contract check: ensure we got data
        if df.empty:
            raise ValueError("No data extracted from SQL Server")
        
        print(f"Extracted {len(df)} records from SQL Server")
        return df.to_dict('records')
    
    @task
    def validate_data_contract(records: List[Dict]) -> List[Dict]:
        """Validate data against contract using Pydantic"""
        validated_records = []
        failed_records = []
        
        for idx, record in enumerate(records):
            try:
                # Validate against contract
                validated_record = CustomerRecord(**record)
                validated_records.append(validated_record.dict())
            except ValidationError as e:
                failed_records.append({
                    'record_index': idx,
                    'record': record,
                    'errors': str(e)
                })
        
        # Contract enforcement: decide on failure threshold
        failure_rate = len(failed_records) / len(records)
        if failure_rate > 0.05:  # More than 5% failures
            raise ValueError(
                f"Data contract validation failed: {len(failed_records)} "
                f"out of {len(records)} records failed validation. "
                f"Failed records: {failed_records[:5]}"
            )
        
        if failed_records:
            print(f"Warning: {len(failed_records)} records failed validation but "
                  f"within acceptable threshold")
        
        print(f"Validated {len(validated_records)} records successfully")
        return validated_records
    
    @task
    def apply_data_quality_checks(records: List[Dict]) -> List[Dict]:
        """Apply additional data quality checks using Great Expectations"""
        df = pd.DataFrame(records)
        ge_df = ge.from_pandas(df)
        
        # Define expectations (data quality rules)
        expectations = {
            'customer_id_unique': ge_df.expect_column_values_to_be_unique('customer_id'),
            'no_null_emails': ge_df.expect_column_values_to_not_be_null('email'),
            'valid_date_range': ge_df.expect_column_values_to_be_between(
                'created_date',
                min_value=datetime(2020, 1, 1),
                max_value=datetime.now()
            ),
            'purchase_amount_reasonable': ge_df.expect_column_values_to_be_between(
                'total_purchases',
                min_value=0,
                max_value=1000000
            )
        }
        
        # Check results
        failed_expectations = [
            name for name, result in expectations.items() 
            if not result['success']
        ]
        
        if failed_expectations:
            raise ValueError(f"Data quality checks failed: {failed_expectations}")
        
        print("All data quality checks passed")
        return records
    
    @task
    def get_api_token() -> str:
        """Authenticate with API"""
        auth_response = requests.post(
            'http://localhost:3011/auth',
            json={
                'client_id': 'your_client_id',
                'client_secret': 'your_secret'
            }
        )
        auth_response.raise_for_status()
        return auth_response.json()['access_token']
    
    @task
    def send_to_api(records: List[Dict], token: str) -> Dict:
        """Send validated data to API"""
        # Create payload matching API contract
        payload = APIPayload(
            customers=records,
            batch_id=f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            record_count=len(records)
        )
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'http://localhost:3011/customers',
            json=payload.dict(),
            headers=headers
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"Successfully sent {len(records)} records to API")
        return result
    
    # Pipeline flow
    raw_data = extract_from_sql()
    validated_data = validate_data_contract(raw_data)
    quality_checked_data = apply_data_quality_checks(validated_data)
    token = get_api_token()
    result = send_to_api(quality_checked_data, token)