from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central application configuration.
    Values are loaded from environment variables / .env file.
    """
    app_name: str = "Enterprise API Integration Platform"
    database_url: str = "postgresql://nexus_user:nexus_pass@localhost:5432/nexus_db"

    secret_key: str = "insecure-dev-key-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
