import os

required_envs = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "REDIS_URL",
    "GOOGLE_AUTH_CLIENT_ID",
    "GOOGLE_AUTH_REDIRECT_URL",
    "ENCRYPTION_KEY",
]

def validate_required_envs():
    for env in required_envs:
        if env not in os.environ:
            raise Exception(f"Environment variable {env} is required")
