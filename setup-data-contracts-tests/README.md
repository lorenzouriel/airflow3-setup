# Airflow Data Pipeline with Data Contracts and Testing
A production-ready Airflow pipeline that extracts data from SQL Server, validates it using data contracts, and sends it to an external API with comprehensive testing.

## Features
- **Data Contracts**: Using Pydantic for schema validation
- **Data Quality Checks**: Using Great Expectations
- **Comprehensive Testing**: Unit, integration, and data quality tests

## Project Structure
```bash
.
├── dags/
│   └── customer_sync.py              # Main Airflow DAG
├── tests/
│   ├── test_customer_sync_dag.py     # Integration tests
├── requirements.txt                  # Python dependencies
├── pytest.ini                        # Pytest configuration
├── docker-compose.yml                # Extended Airflow configs
├── Dockerfile                        # Airflow 3 official image
└── README.md                         # This file
```

## Installation
### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Airflow
```bash
docker-compose up -d --build
```

### 4. Configure Airflow Connections
#### SQL Server Connection
```bash
airflow connections add 'sql_server_conn' \
    --conn-type 'mssql' \
    --conn-host 'your-sql-server.database.windows.net' \
    --conn-schema 'your_database' \
    --conn-login 'your_username' \
    --conn-password 'your_password' \
    --conn-port 1433
```

Or via Airflow UI:
1. Go to Admin → Connections
2. Click the "+" button
3. Fill in:
   - **Connection Id**: `sql_server_conn`
   - **Connection Type**: `Microsoft SQL Server`
   - **Host**: `your-sql-server.database.windows.net`
   - **Schema**: `your_database`
   - **Login**: `your_username`
   - **Password**: `your_password`
   - **Port**: `1433`

## Configuration
### Environment Variables
Create a `.env` file (optional):
```bash
# API Configuration
API_BASE_URL=https://localhost:3011
API_CLIENT_ID=your_client_id
API_CLIENT_SECRET=your_secret

# PostgreSQL
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
POSTGRES_HOST=postgres

# Airflow User (created during init)
_AIRFLOW_WWW_USER_USERNAME=airflow-dev
_AIRFLOW_WWW_USER_PASSWORD=airflow-dev

# Airflow UID (optional, used for file permissions)
AIRFLOW_UID=50000

# Airflow configuration
AIRFLOW__API_AUTH__JWT_SECRET=
AIRFLOW__CORE__FERNET_KEY=
```

### Database Setup
Ensure your SQL Server has the required table:
```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    email NVARCHAR(255) NOT NULL,
    name NVARCHAR(100) NOT NULL,
    created_date DATETIME NOT NULL,
    total_purchases DECIMAL(10,2) NOT NULL,
    status NVARCHAR(50) NOT NULL,
    updated_date DATETIME NOT NULL DEFAULT GETDATE()
);

-- Create index for better performance
CREATE INDEX idx_updated_date ON customers(updated_date);

-- Sample data
INSERT INTO customers (customer_id, email, name, created_date, total_purchases, status, updated_date)
VALUES 
    (1, 'john.doe@example.com', 'John Doe', '2023-01-15', 1500.50, 'active', GETDATE()),
    (2, 'jane.smith@example.com', 'Jane Smith', '2023-02-20', 2300.75, 'active', GETDATE()),
    (3, 'bob.johnson@example.com', 'Bob Johnson', '2023-03-10', 890.25, 'inactive', GETDATE());
```

## Running the Pipeline
### Run the DAG
#### Via UI:
1. Open http://localhost:8080
2. Login (admin/admin)
3. Find `customer_sync_with_contracts` DAG
4. Toggle it ON
5. Click the "Play" button to trigger manually

#### Via CLI:
```bash
# Trigger the DAG manually
airflow dags trigger customer_sync_with_contracts

# Run a specific task for testing
airflow tasks test customer_sync_with_contracts extract_from_sql 2024-01-01

# Check DAG status
airflow dags list

# View task instances
airflow tasks list customer_sync_with_contracts
```

## Running Tests
### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/test_customer_sync_tasks.py -v

# Integration tests only
pytest tests/test_customer_sync_dag.py -v

# Data quality tests only
pytest tests/test_data_quality.py -v
```

### Run with Coverage
```bash
pytest --cov=dags --cov-report=html --cov-report=term tests/
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Specific Test
```bash
pytest tests/test_customer_sync_tasks.py::TestDataContracts::test_valid_customer_record -v
```

## CI/CD Integration
### GitHub Actions Example
```yaml
name: Test Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v --cov=dags
```