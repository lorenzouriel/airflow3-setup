# Apache Airflow 3.0 with Notifications

Apache Airflow 3.0 setup with integrated notification systems for Email, Slack, and Microsoft Teams. This configuration demonstrates how to implement failure alerts and monitoring across multiple communication channels.

## Features

- **Multiple Notification Channels**: Email, Slack, and Microsoft Teams
- **Task Failure Alerts**: Automatic notifications on task failures
- **DAG Failure Callbacks**: Configure alerts at DAG or task level
- **LocalExecutor**: Efficient task execution for single-machine deployments
- **PostgreSQL Backend**: Reliable metadata storage
- **SMTP Integration**: Email notifications support

## Project Structure

```
setup-notifications/
├── dags/
│   ├── email.py              # Email notification implementation
│   ├── email_conn.py         # Email with connection configuration
│   ├── slack.py              # Slack integration
│   ├── teams.py              # Microsoft Teams integration
│   ├── notifier.py           # Consolidated notification functions
│   └── notifier_dag.py       # Example DAG with alerts
├── config/
│   ├── airflow.cfg          # Custom Airflow configuration
│   └── webserver_config.py  # Webserver authentication config
├── include/                  # Additional Python modules
├── plugins/                  # Custom Airflow plugins
├── logs/                     # Airflow logs
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
└── .env
```

## Requirements

- Docker >= 24.x
- Docker Compose >= 2.x
- Slack Webhook URL (for Slack notifications)
- Microsoft Teams Webhook URL (for Teams notifications)
- SMTP credentials (for email notifications)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lorenzouriel/airflow3-setup.git
cd airflow3-setup/setup-notifications
```

### 2. Configure Environment Variables

Create or update the `.env` file:

```bash
# PostgreSQL
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

# Airflow Core
AIRFLOW_UID=50000
AIRFLOW__CORE__FERNET_KEY=your_fernet_key_here
AIRFLOW__API_AUTH__JWT_SECRET=your_jwt_secret_here

# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_STARTTLS=True
SMTP_SSL=False
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_PORT=587
SMTP_MAIL_FROM=your_email@gmail.com
```

### 3. Set Up Notification Webhooks

Create Airflow Variables for your notification services:

1. Start Airflow (see Usage section)
2. Navigate to Admin > Variables in the Airflow UI
3. Add the following variables:

| Key | Value |
|-----|-------|
| `slack_webhook_url` | Your Slack Webhook URL |
| `teams_webhook_url` | Your Microsoft Teams Webhook URL |

Alternatively, set them via CLI:

```bash
docker exec -it airflow-webserver airflow variables set slack_webhook_url "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
docker exec -it airflow-webserver airflow variables set teams_webhook_url "https://outlook.office.com/webhook/YOUR/WEBHOOK/URL"
```

## Usage

### Initialize Airflow

```bash
docker compose up airflow-init
```

### Start Services

```bash
docker compose up -d
```

### Access Web UI

Open [http://localhost:8080](http://localhost:8080)

Default credentials:
```
Username: admin
Password: admin
```

## Notification Examples

### Email Notifications

```python
from dags.notifier import failure_email

@task(on_failure_callback=failure_email)
def my_task():
    # Your task logic
    pass
```

### Slack Notifications

```python
from dags.notifier import slack_fail_alert

@dag(
    dag_id="my_dag",
    default_args={"on_failure_callback": slack_fail_alert}
)
def my_dag():
    # Your DAG logic
    pass
```

### Microsoft Teams Notifications

```python
from dags.notifier import task_fail_alert_teams

@task(on_failure_callback=task_fail_alert_teams)
def my_task():
    # Your task logic
    pass
```

## Configuration

### Setting Up Slack

1. Create a Slack App in your workspace
2. Enable Incoming Webhooks
3. Create a webhook for your channel
4. Add the webhook URL to Airflow Variables

### Setting Up Microsoft Teams

1. Open the Teams channel where you want notifications
2. Click on the ellipsis (...) next to the channel name
3. Select "Connectors" > "Incoming Webhook"
4. Configure the webhook and copy the URL
5. Add the webhook URL to Airflow Variables

### Setting Up Email (Gmail)

1. Enable 2-Factor Authentication in your Google Account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security > 2-Step Verification > App passwords
   - Generate a new app password for "Mail"
3. Use the app password in your `.env` file

## Available Notification Functions

Located in [dags/notifier.py](dags/notifier.py):

- `failure_email(context)`: Send email on task failure
- `slack_fail_alert(context)`: Send Slack message on failure
- `task_fail_alert_teams(context)`: Send Teams message on failure

## Testing Notifications

Run the example DAG:

1. Enable the `example_alerts` DAG in the UI
2. Trigger the DAG manually
3. The task will intentionally fail and trigger your configured notification

## Common Commands

| Action | Command |
|--------|---------|
| View scheduler logs | `docker logs airflow-scheduler -f` |
| View webserver logs | `docker logs airflow-webserver -f` |
| Test email config | `docker exec -it airflow-webserver airflow config get-value smtp smtp_host` |
| List variables | `docker exec -it airflow-webserver airflow variables list` |
| Restart services | `docker compose restart` |

## Troubleshooting

### Email Not Sending

Check SMTP configuration:

```bash
docker exec -it airflow-webserver airflow config get-value smtp smtp_host
docker logs airflow-scheduler --tail=100 | grep -i smtp
```

### Slack Notifications Not Working

Verify webhook URL:

```bash
docker exec -it airflow-webserver airflow variables get slack_webhook_url
```

Test webhook manually:

```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test notification"}' \
  YOUR_SLACK_WEBHOOK_URL
```

### Teams Notifications Not Working

Verify webhook URL:

```bash
docker exec -it airflow-webserver airflow variables get teams_webhook_url
```

## Cleanup

```bash
# Stop services
docker compose down

# Remove all data
docker compose down -v
```

## Next Steps

- Customize notification messages in [dags/notifier.py](dags/notifier.py)
- Add custom notification channels
- Configure notification templates
- Set up SLA alerts
- Implement success notifications

## Resources

- [Airflow Notifications Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/notifications.html)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [Microsoft Teams Webhooks](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)
