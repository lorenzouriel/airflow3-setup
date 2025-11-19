# Apache Airflow 3.0 - Setup Collection

A comprehensive collection of Apache Airflow 3.0 configurations and setups for different use cases. This repository serves as a learning resource and quick-start template for various Airflow deployment scenarios.

## Repository Structure

```
airflow3/
├── setup-basic-pocket/          # Lightweight Airflow + PostgreSQL
├── setup-basic-local-executor/  # Full-featured LocalExecutor setup
├── setup-celery-executor/       # Production-grade CeleryExecutor
├── setup-notifications/         # Email, Slack, and Teams alerts
└── setup-sso/                   # SSO authentication integration
```

## Available Setups

### [setup-basic-pocket](setup-basic-pocket/)
**Lightweight Airflow for Quick Deployments**

A minimal Apache Airflow setup with PostgreSQL, perfect for:
- Local development and testing
- CI/CD experimentation
- Lightweight servers or VPS environments
- Learning Airflow basics

**Key Features:**
- Apache Airflow 2.10.2 with LocalExecutor
- PostgreSQL backend
- Minimal configuration
- Fast startup time

[View Documentation](setup-basic-pocket/README.md)

---

### [setup-basic-local-executor](setup-basic-local-executor/)
**Complete LocalExecutor Configuration**

Full-featured Airflow 3.0 setup with advanced capabilities:
- Apache Airflow 3.0 with LocalExecutor
- SMTP email notifications
- Custom configurations via airflow.cfg
- Execution API for improved performance
- Health checks and monitoring

**Ideal For:**
- Production single-machine deployments
- Teams needing email notifications
- Custom configuration requirements
- API-driven integrations

[View Documentation](setup-basic-local-executor/README.md)

---

### [setup-celery-executor](setup-celery-executor/)
**Production-Grade Distributed Execution**

Enterprise-ready Airflow setup with CeleryExecutor for distributed task processing:
- Horizontal scaling with worker pools
- Redis as message broker
- Flower for worker monitoring
- High availability configuration
- Advanced metrics and monitoring

**Ideal For:**
- Production environments
- High-volume task processing
- Distributed workloads
- Enterprise deployments

[View Documentation](setup-celery-executor/README.md)

---

### [setup-notifications](setup-notifications/)
**Multi-Channel Alert System**

Airflow setup demonstrating integration with multiple notification channels:
- Email notifications via SMTP
- Slack webhooks integration
- Microsoft Teams alerts
- Custom notification callbacks
- Failure monitoring examples

**Ideal For:**
- Team collaboration
- Real-time failure alerts
- Multi-channel communication
- DevOps monitoring workflows

[View Documentation](setup-notifications/README.md)

---

### [setup-sso](setup-sso/)
**Enterprise Authentication Integration**

Airflow with Single Sign-On (SSO) authentication:
- OAuth 2.0 integration (Google, GitHub, Azure AD, Okta)
- Role-based access control
- Custom webserver configuration
- Enterprise security features
- Auto-user registration

**Ideal For:**
- Enterprise environments
- Organizations using SSO
- Advanced security requirements
- Multi-team deployments

[View Documentation](setup-sso/README.md)

---

## Quick Start Guide

### Choose Your Setup

1. **Just Learning?** → Start with [setup-basic-pocket](setup-basic-pocket/)
2. **Need Email Alerts?** → Use [setup-basic-local-executor](setup-basic-local-executor/)
3. **Scaling for Production?** → Deploy [setup-celery-executor](setup-celery-executor/)
4. **Want Notifications?** → Try [setup-notifications](setup-notifications/)
5. **Enterprise SSO?** → Configure [setup-sso](setup-sso/)

### Basic Installation Steps

Each setup follows a similar pattern:

```bash
# 1. Clone the repository
git clone https://github.com/lorenzouriel/airflow3-setup.git
cd airflow3-setup/<setup-name>

# 2. Configure environment
cp .example-env .env  # If available
# Edit .env with your settings

# 3. Initialize Airflow
docker compose up airflow-init

# 4. Start services
docker compose up -d

# 5. Access Web UI
# Open http://localhost:8080
# Default: admin/admin
```

## Common Requirements

All setups require:
- **Docker** >= 24.x
- **Docker Compose** >= 2.x
- **Linux, macOS, or Windows with WSL2**

## Feature Comparison

| Feature | Pocket | Local Executor | Celery Executor | Notifications | SSO |
|---------|--------|----------------|-----------------|---------------|-----|
| Airflow Version | 2.10.2 | 3.0 | 3.0 | 3.0 | 3.0 |
| Executor | Local | Local | Celery | Local | Local |
| PostgreSQL | ✅ | ✅ | ✅ | ✅ | ✅ |
| Redis | ❌ | ❌ | ✅ | ❌ | ❌ |
| Email Alerts | ❌ | ✅ | ✅ | ✅ | ❌ |
| Slack Integration | ❌ | ❌ | ❌ | ✅ | ❌ |
| Teams Integration | ❌ | ❌ | ❌ | ✅ | ❌ |
| SSO Auth | ❌ | ❌ | ❌ | ❌ | ✅ |
| Horizontal Scaling | ❌ | ❌ | ✅ | ❌ | ❌ |
| Worker Monitoring | ❌ | ❌ | ✅ (Flower) | ❌ | ❌ |
| Metrics & Stats | ❌ | ❌ | ✅ (StatsD) | ❌ | ❌ |
| API Server | ❌ | ✅ | ✅ | ✅ | ✅ |

## Repository Purpose

This repository is designed to:
- **Learn**: Understand different Airflow configurations
- **Compare**: See trade-offs between different setups
- **Deploy**: Quick-start production-ready configurations
- **Customize**: Use as templates for your own deployments

## Common Operations

### View Logs
```bash
docker logs airflow-webserver -f
docker logs airflow-scheduler -f
```

### Access Airflow CLI
```bash
docker exec -it airflow-webserver airflow <command>
```

### Stop Services
```bash
docker compose down
```

### Remove All Data
```bash
docker compose down -v
```

## Customization Tips

### Adding Python Dependencies

Add packages to `requirements.txt`:
```txt
pandas==2.0.0
requests==2.31.0
apache-airflow-providers-amazon
```

Then rebuild:
```bash
docker compose up -d --build
```

### Custom DAGs

Place DAG files in the `dags/` directory:
```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="my_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    task = BashOperator(
        task_id="my_task",
        bash_command="echo 'Hello Airflow!'"
    )
```

### Environment Variables

Each setup uses `.env` files for configuration. Common variables:

```bash
# PostgreSQL
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

# Airflow
AIRFLOW_UID=50000
AIRFLOW__CORE__FERNET_KEY=<generate-key>
```

Generate Fernet key:
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Troubleshooting

### Permission Errors
```bash
sudo chown -R 50000:0 logs
sudo chmod -R 775 logs
```

### Database Connection Issues
```bash
docker logs postgres
docker exec -it postgres psql -U airflow -d airflow
```

### Port Conflicts
If port 8080 is in use, modify `docker-compose.yaml`:
```yaml
ports:
  - "8081:8080"  # Change 8081 to your preferred port
```

## Contributing

Feel free to:
- Open issues for questions or bugs
- Submit pull requests for improvements
- Share your own configurations
- Suggest new setup scenarios

## Inspirations & Credits

This setup collection is built from knowledge and examples from the community:
- [matsudan/airflow-dag-examples](https://github.com/matsudan/airflow-dag-examples)
- [FabioCantarimM/airflow3](https://github.com/FabioCantarimM/airflow3)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- Various community contributions and best practices

## Resources

### Official Documentation
- [Apache Airflow](https://airflow.apache.org/)
- [Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Learning Resources
- [Airflow Summit Videos](https://www.youtube.com/c/Airflow)
- [Astronomer Academy](https://academy.astronomer.io/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

### Community
- [Airflow Slack](https://apache-airflow-slack.herokuapp.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/airflow)
- [GitHub Discussions](https://github.com/apache/airflow/discussions)

## License

This repository is for educational and personal use. Feel free to fork, modify, and adapt for your needs.

## Author

Created and maintained for learning purposes and sharing with the community.

---

**Note**: These setups are intended for learning and development. For production deployments, ensure you implement proper security measures, backups, monitoring, and follow your organization's best practices.
