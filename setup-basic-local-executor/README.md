# Apache Airflow 3.0 with LocalExecutor

A complete Apache Airflow 3.0 setup using LocalExecutor with PostgreSQL backend and Docker Compose. This configuration includes advanced features like SMTP email notifications, custom configurations, and execution API.

## Features

- **Apache Airflow 3.0** with LocalExecutor
- **PostgreSQL 15** as metadata database
- **SMTP Email Integration** for task notifications
- **Custom Configuration** support via airflow.cfg
- **Execution API Server** for improved task execution
- **Health Checks** for scheduler monitoring
- **JWT Authentication** for API security

## Project Structure

```
setup-basic-local-executor/
├── dags/              # DAG files
├── logs/              # Airflow logs
├── config/            # Custom Airflow configuration
├── plugins/           # Custom plugins
├── include/           # Additional Python modules
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
└── .env
```

## Requirements

- Docker >= 24.x
- Docker Compose >= 2.x
- Linux, macOS, or Windows with WSL2

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lorenzouriel/airflow3-setup.git
cd airflow3-setup/setup-basic-local-executor
```

### 2. Set Up Environment Variables

Create or update the `.env` file with your configuration:

```bash
# PostgreSQL Configuration
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
POSTGRES_HOST=postgres

# Airflow Configuration
AIRFLOW_UID=50000
AIRFLOW__CORE__FERNET_KEY=your_fernet_key_here
AIRFLOW__API_AUTH__JWT_SECRET=your_jwt_secret_here

# SMTP Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_STARTTLS=True
SMTP_SSL=False
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_PORT=587
SMTP_MAIL_FROM=your_email@gmail.com
```

### 3. Generate Keys

Generate a Fernet key:

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Generate a JWT secret:

```bash
openssl rand -hex 32
```

### 4. Create Required Directories

```bash
mkdir -p dags logs config plugins include
```

### 5. Set Proper Permissions

```bash
sudo chown -R 50000:0 logs
sudo chmod -R 775 logs
```

## Usage

### Initialize Airflow Database

```bash
docker compose up airflow-init
```

### Start All Services

```bash
docker compose up -d
```

### Check Services Status

```bash
docker ps
```

You should see the following containers running:
- `airflow-webserver`
- `airflow-scheduler`
- `airflow-apiserver`
- `postgres`

## Access the Web UI

Open your browser and navigate to:

👉 [http://localhost:8080](http://localhost:8080)

Default credentials:
```
Username: admin
Password: admin
```

## Configuration

### Custom Airflow Configuration

You can customize Airflow settings by editing the `config/airflow.cfg` file or adding environment variables to the `.env` file.

### Email Notifications

To enable email notifications:

1. Configure SMTP settings in `.env`
2. Use `email_on_failure` or `email_on_retry` in your DAG default_args

Example:
```python
default_args = {
    'email': ['your_email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}
```

## Common Commands

| Action | Command |
|--------|---------|
| View logs | `docker logs airflow-webserver -f` |
| Restart services | `docker compose restart` |
| Stop services | `docker compose down` |
| Remove volumes | `docker compose down -v` |
| Access Airflow shell | `docker exec -it airflow-webserver bash` |
| Access PostgreSQL | `docker exec -it airflow-metabase-1 psql -U airflow -d airflow` |

## Troubleshooting

### Permission Issues

If you encounter permission errors with logs:

```bash
sudo chown -R 50000:0 logs
sudo chmod -R 775 logs
```

### Database Connection Error

Ensure PostgreSQL is healthy:

```bash
docker logs airflow-metabase-1
```

### Scheduler Not Running

Check scheduler logs:

```bash
docker logs airflow-scheduler --tail=100
```

## Cleanup

Stop and remove all containers:

```bash
docker compose down
```

Remove all data including volumes:

```bash
docker compose down -v
```

## Next Steps

- Add custom DAGs to the `dags/` directory
- Install additional Python packages in `requirements.txt`
- Configure connections via Airflow UI
- Set up custom plugins in `plugins/` directory
- Customize Airflow configuration in `config/airflow.cfg`

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow 3.0 Release Notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html)
