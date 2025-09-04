import os
from airflow.providers.fab.auth_manager.security_manager.override import (
        FabAirflowSecurityManagerOverride,
    )
from flask_appbuilder.security.manager import AUTH_OAUTH

AUTH_TYPE = AUTH_OAUTH

AUTH_USER_REGISTRATION_ROLE = "Public"
AUTH_ROLE_PUBLIC = 'Public'
AUTH_ROLE_ADMIN = 'Admin'
AUTH_ROLES_SYNC_AT_LOGIN = True
AUTH_USER_REGISTRATION = True

OAUTH_PROVIDERS = [{
    'name': 'azure',
    'icon': 'fa-windows',
    'token_key': 'access_token',
    'remote_app': {
        'api_base_url': "https://login.microsoftonline.com/{}/".format(os.getenv("AIRFLOW_SSO_AAD_TENANT_ID")),
        'request_token_url': None,
        'request_token_params': {
            'scope': 'openid email profile'
        },
        'access_token_url': "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(os.getenv("AIRFLOW_SSO_AAD_TENANT_ID")),
        'authorize_url': "https://login.microsoftonline.com/{}/oauth2/v2.0/authorize".format(os.getenv("AIRFLOW_SSO_AAD_TENANT_ID")),
        'authorize_params': {
            'scope': 'openid email profile'
        },
        'client_id': os.getenv("AIRFLOW_SSO_AAD_CLIENT_ID"),
        'client_secret': os.getenv("AIRFLOW_SSO_AAD_CLIENT_SECRET"),
        'jwks_uri': 'https://login.microsoftonline.com/common/discovery/v2.0/keys',
        'redirect_uri': 'http://localhost:8080/auth/oauth-authorized/azure',
    }
}]

AUTH_ROLES_MAPPING = {
    "airflow_prod_admin": ["Admin"],
    "airflow_prod_user": ["Op"],
    "airflow_prod_viewer": ["Viewer"],
}

class CustomSecurityManager(FabAirflowSecurityManagerOverride):
    def get_oauth_user_info(self, provider, response=None):
        try:
            me = super().get_oauth_user_info(provider, response)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.log.debug(e)
            me = {}

        return {
            "name": me.get("first_name", "") + " " + me.get("last_name", ""),
            "email": me.get("email"),
            "first_name": me.get("first_name"),
            "last_name": me.get("last_name"),
            "id": me.get("username"),
            "username": me.get("email"),
            "role_keys": me.get("role_keys", ["Public"]),
        }

FAB_SECURITY_MANAGER_CLASS = 'webserver_config.CustomSecurityManager'
SECURITY_MANAGER_CLASS = CustomSecurityManager