# Apache Airflow + PostgreSQL — Docker Setup

A lightweight, up-to-date configuration for running **Apache Airflow** with a **PostgreSQL** backend using Docker Compose.

This setup is ideal for:

* Local development and testing
* CI/CD experimentation
* Lightweight servers or VPS environments (e.g., Ubuntu)

## Project Structure
```
airflow/
├─ dags/
│   └─ example_dag.py
├─ logs/
├─ docker-compose.yml
└─ .env
```

## Requirements
* **Docker** ≥ 24.x
* **Docker Compose** ≥ 2.x
* Linux or macOS (tested on Ubuntu 22.04+)

## Installation

### Clone the project (or create a new folder)
```bash
mkdir ~/vps/airflow && cd ~/vps/airflow
```

### Create directories
```bash
mkdir -p dags logs
```

### Add the following files
#### `.env`
```bash
AIRFLOW_UID=50000
```

#### `docker-compose.yml`
```yaml
version: "3.9"

x-airflow-common:
  &airflow-common
  image: apache/airflow:2.10.2
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: LocalExecutor
    AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CORE__FERNET_KEY: ''
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth'
    _PIP_ADDITIONAL_REQUIREMENTS: ""
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
  user: "${AIRFLOW_UID:-50000}:0"
  depends_on:
    postgres:
      condition: service_healthy

services:
  postgres:
    image: postgres:16
    container_name: postgres
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U airflow"]
      interval: 5s
      retries: 5
      start_period: 5s
    volumes:
      - postgres_data:/var/lib/postgresql/data

  airflow-webserver:
    <<: *airflow-common
    container_name: airflow-webserver
    command: webserver
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 10s
      timeout: 10s
      retries: 5
    restart: always

  airflow-scheduler:
    <<: *airflow-common
    container_name: airflow-scheduler
    command: scheduler
    restart: always

  airflow-init:
    <<: *airflow-common
    container_name: airflow-init
    command: bash -c "airflow db upgrade && airflow users create \
                      --username admin \
                      --firstname Air \
                      --lastname Flow \
                      --role Admin \
                      --email admin@example.com \
                      --password admin || true"
    restart: "no"

volumes:
  postgres_data:
```

**OBS**: If the user was not created, run:
```bash
docker exec -it airflow-webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

## Generate a Fernet Key (Optional but Recommended)

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the result and paste it inside the `AIRFLOW__CORE__FERNET_KEY` value in `docker-compose.yml`.

## Usage

### Initialize the Airflow Database

```bash
docker compose up airflow-init
```

### Start All Services

```bash
docker compose up -d
```

### Check Containers

```bash
docker ps
```

You should see:

```
airflow-webserver   Up (healthy)
airflow-scheduler   Up (healthy)
postgres            Up (healthy)
```

## Access the Web UI

Open your browser:

👉 [http://localhost:8080](http://localhost:8080)

Login credentials:

```
Username: admin
Password: admin
```

If you’re running this on a remote VPS, use your server’s IP:

```
http://<server-ip>:8080
```

## Example DAG
`dags/example_dag.py`:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="example_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    t1 = BashOperator(
        task_id="hello",
        bash_command="echo 'Airflow is running successfully!'"
    )
```

## Cleanup

To stop and remove containers:

```bash
docker compose down
```

To remove all volumes (including database data):

```bash
docker compose down -v
```

## Troubleshooting

### Permission denied: `/opt/airflow/logs/...`

Run:

```bash
sudo chown -R 50000:0 logs
sudo chmod -R 775 logs
```

### Webserver unhealthy

Check logs:

```bash
docker logs airflow-webserver --tail=50
```

Likely cause: invalid Fernet key or DB connection not ready.

### Database connection error

Ensure Postgres is healthy:

```bash
docker logs postgres
```

## Useful Commands

| Action                  | Command                                                      |
| ----------------------- | ------------------------------------------------------------ |
| Check logs of a service | `docker logs airflow-webserver -f`                           |
| Restart Airflow         | `docker compose restart airflow-webserver airflow-scheduler` |
| List running containers | `docker ps`                                                  |
| Open Airflow shell      | `docker exec -it airflow-webserver bash`                     |
| Access Postgres shell   | `docker exec -it postgres psql -U airflow -d airflow`        |

## Environment Variables

| Variable                    | Description                            | Default   |
| --------------------------- | -------------------------------------- | --------- |
| `AIRFLOW_UID`               | Host user ID for mounted volumes       | `50000`   |
| `POSTGRES_USER`             | PostgreSQL username                    | `airflow` |
| `POSTGRES_PASSWORD`         | PostgreSQL password                    | `airflow` |
| `POSTGRES_DB`               | PostgreSQL database name               | `airflow` |
| `AIRFLOW__CORE__FERNET_KEY` | Encryption key for Airflow connections | *(empty)* |

## Next Steps
* Add custom Python dependencies by extending the Airflow image:

  ```Dockerfile
  FROM apache/airflow:2.10.2
  RUN pip install pandas requests
  ```
* Integrate with Celery + Redis for distributed execution
* Connect to external services (S3, BigQuery, etc.)
* Configure automatic backups for PostgreSQL
