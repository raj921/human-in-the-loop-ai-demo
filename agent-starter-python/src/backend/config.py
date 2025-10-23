from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "frontdesk-backend"
    database_url: str = "sqlite:///./data.db"
    supervisor_webhook_url: str | None = None
    notify_console_fallback: bool = True
    request_timeout_seconds: int = 60 * 60 * 4  # 4 hours default

    class Config:
        env_prefix = "FD_"
        env_file = ".env.local"


settings = Settings()


