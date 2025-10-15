# GuardFlow Security Configuration
SECURITY_CONFIG = {
    "oauth2": {
        "client_id": "guardflow_client",
        "client_secret": "guardflow_secret_2024",
        "authorization_url": "https://auth.guardflow.com/oauth/authorize",
        "token_url": "https://auth.guardflow.com/oauth/token",
        "scopes": ["read", "write", "admin"]
    },
    "jwt": {
        "secret_key": "guardflow_jwt_secret_2024",
        "algorithm": "HS256",
        "access_token_expire_minutes": 30,
        "refresh_token_expire_days": 7
    },
    "rbac": {
        "roles": ["admin", "manager", "user", "guest"],
        "permissions": {
            "admin": ["*"],
            "manager": ["read", "write", "manage_users"],
            "user": ["read", "write"],
            "guest": ["read"]
        }
    }
}


