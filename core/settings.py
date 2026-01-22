from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid",  # keep strict (best practice)
    )

    # App
    app_name: str = "Judge Server"
    debug: bool = False
    log_level: str = "INFO"

    # Database / Redis
    database_url: str
    redis_url: str = "redis://redis:6379/0"

    # Celery (allow override)
    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    # Judge limits
    judge_time_limit_sec: int = 2
    judge_memory_limit_mb: int = 256
    judge_cpu_limit: float = 0.5

    def model_post_init(self, __context):
        # If not explicitly set, use REDIS_URL
        if self.celery_broker_url is None:
            self.celery_broker_url = self.redis_url
        if self.celery_result_backend is None:
            self.celery_result_backend = self.redis_url


settings = Settings()

