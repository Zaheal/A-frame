from fastapi_users.authentication import JWTStrategy
from src.config.auth_config import get_auth_settings

settings = get_auth_settings()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=3600)
