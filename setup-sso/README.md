# Apache Airflow 3.0 with SSO Authentication

Apache Airflow 3.0 setup with Single Sign-On (SSO) authentication integration. This configuration demonstrates how to implement enterprise-grade authentication using OAuth providers like Google, GitHub, or custom OIDC providers.

## Features

- **SSO Authentication**: OAuth/OIDC integration for enterprise authentication
- **Custom Webserver Configuration**: Extended authentication settings
- **FAB Auth Manager**: Flask-AppBuilder authentication backend
- **LocalExecutor**: Efficient single-machine task execution
- **PostgreSQL Backend**: Reliable metadata storage
- **Secure Configuration**: JWT authentication for API access

## Project Structure

```
setup-sso/
├── config/
│   ├── airflow.cfg          # Custom Airflow configuration
│   └── webserver_config.py  # SSO and authentication configuration
├── dags/                     # DAG files
├── include/                  # Additional Python modules
├── plugins/                  # Custom Airflow plugins
├── logs/                     # Airflow logs
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── .env
└── .example-env             # Example environment variables
```

## Requirements

- Docker >= 24.x
- Docker Compose >= 2.x
- OAuth provider credentials (Google, GitHub, Azure AD, Okta, etc.)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lorenzouriel/airflow3-setup.git
cd airflow3-setup/setup-sso
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .example-env .env
```

Edit `.env` with your configuration:

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

# OAuth Configuration (example for Google)
OAUTH_CLIENT_ID=your_client_id.apps.googleusercontent.com
OAUTH_CLIENT_SECRET=your_client_secret
OAUTH_REDIRECT_URI=http://localhost:8080/oauth-authorized/google
```

### 3. Configure SSO Provider

Edit `config/webserver_config.py` to configure your OAuth provider. The file includes examples for:

- **Google OAuth**
- **GitHub OAuth**
- **Azure AD**
- **Okta**
- **Generic OIDC**

Example for Google OAuth:

```python
from airflow.www.security import AirflowSecurityManager
from flask_appbuilder.security.manager import AUTH_OAUTH

AUTH_TYPE = AUTH_OAUTH
OAUTH_PROVIDERS = [
    {
        'name': 'google',
        'token_key': 'access_token',
        'icon': 'fa-google',
        'remote_app': {
            'client_id': os.getenv('OAUTH_CLIENT_ID'),
            'client_secret': os.getenv('OAUTH_CLIENT_SECRET'),
            'api_base_url': 'https://www.googleapis.com/oauth2/v2/',
            'client_kwargs': {'scope': 'email profile'},
            'request_token_url': None,
            'access_token_url': 'https://accounts.google.com/o/oauth2/token',
            'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        }
    }
]
```

### 4. Set Up OAuth Application

#### For Google OAuth:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to Credentials > Create Credentials > OAuth 2.0 Client ID
5. Set authorized redirect URI: `http://localhost:8080/oauth-authorized/google`
6. Copy Client ID and Client Secret to `.env`

#### For GitHub OAuth:

1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Click "New OAuth App"
3. Set Authorization callback URL: `http://localhost:8080/oauth-authorized/github`
4. Copy Client ID and Client Secret to `.env`

### 5. Create Required Directories

```bash
mkdir -p dags logs config plugins include
```

### 6. Set Permissions

```bash
sudo chown -R 50000:0 logs
sudo chmod -R 775 logs
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

You will be redirected to your OAuth provider for authentication.

## Configuration

### Webserver Configuration

The `config/webserver_config.py` file controls authentication behavior:

- **AUTH_TYPE**: Authentication method (AUTH_OAUTH, AUTH_DB, etc.)
- **OAUTH_PROVIDERS**: List of OAuth provider configurations
- **AUTH_USER_REGISTRATION**: Auto-register users on first login
- **AUTH_USER_REGISTRATION_ROLE**: Default role for new users

### Role-Based Access Control

Configure user roles in `webserver_config.py`:

```python
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Viewer"  # Admin, Op, User, Viewer, Public
```

### Allowed Email Domains

Restrict access to specific domains:

```python
AUTH_LDAP_ALLOW_SELF_SIGNED = True
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Viewer"

# In your custom security manager
def oauth_user_info(self, provider, response=None):
    if provider == 'google':
        me = self.appbuilder.sm.oauth_remotes[provider].get('userinfo')
        email = me.data.get('email', '')
        if not email.endswith('@yourdomain.com'):
            return None
    # ... rest of implementation
```

## Security Best Practices

1. **Use HTTPS in Production**: Configure SSL/TLS certificates
2. **Secure Secrets**: Use secret management tools (AWS Secrets Manager, HashiCorp Vault)
3. **Limit OAuth Scopes**: Request only necessary permissions
4. **Regular Token Rotation**: Implement token refresh mechanisms
5. **Audit Logging**: Enable detailed access logs
6. **Network Security**: Use VPC/firewall rules to restrict access

## Common Commands

| Action | Command |
|--------|---------|
| View webserver logs | `docker logs airflow-webserver -f` |
| Check auth config | `docker exec -it airflow-webserver cat /opt/airflow/webserver_config.py` |
| List users | `docker exec -it airflow-webserver airflow users list` |
| Create admin user | `docker exec -it airflow-webserver airflow users create --role Admin --username admin --email admin@example.com --firstname Admin --lastname User --password admin` |
| Restart webserver | `docker compose restart airflow-webserver` |

## Troubleshooting

### OAuth Redirect Error

Ensure your redirect URI matches exactly:
- In OAuth provider settings
- In `.env` OAUTH_REDIRECT_URI
- Must use same protocol (http/https)

### User Not Auto-Registered

Check webserver logs:

```bash
docker logs airflow-webserver --tail=100 | grep -i oauth
```

Verify configuration:

```python
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Viewer"
```

### Cannot Access After Login

Check user roles:

```bash
docker exec -it airflow-webserver airflow users list
```

Update user role if needed:

```bash
docker exec -it airflow-webserver airflow users add-role --username user@example.com --role Admin
```

### Invalid Client Error

Verify OAuth credentials in `.env`:
- Check CLIENT_ID format
- Ensure CLIENT_SECRET is correct
- Verify redirect URI matches

## Production Deployment

For production environments:

1. **Use HTTPS**: Configure SSL certificates
2. **Secure Environment Variables**: Use secrets management
3. **Database Backup**: Regular PostgreSQL backups
4. **Monitoring**: Set up logging and metrics
5. **High Availability**: Consider CeleryExecutor for distributed setup

Example HTTPS redirect URI:
```
https://airflow.yourdomain.com/oauth-authorized/google
```

## Cleanup

```bash
# Stop services
docker compose down

# Remove all data
docker compose down -v
```

## Next Steps

- Configure multiple OAuth providers
- Implement custom authentication logic
- Set up LDAP integration
- Configure team-based access control
- Implement audit logging
- Add MFA (Multi-Factor Authentication)

## Resources

- [Airflow Security Documentation](https://airflow.apache.org/docs/apache-airflow/stable/security/index.html)
- [Flask-AppBuilder Security](https://flask-appbuilder.readthedocs.io/en/latest/security.html)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [Google OAuth Setup](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Setup](https://docs.github.com/en/developers/apps/building-oauth-apps)
