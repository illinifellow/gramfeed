from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GRAMFEED_", env_file=".env")

    database_url: str = "postgresql+asyncpg://gramfeed:gramfeed@localhost/gramfeed"
    redis_url: str = "redis://localhost:6379/0"
    public_url: str = "http://localhost:8000"
    admin_token: str = "change-me"
    # media is re-hosted: Instagram CDN links expire within hours, feed readers fetch days later
    s3_bucket: str = "gramfeed-media"
    s3_endpoint: str | None = None
    s3_public_url: str | None = None
    # one logged-in session lowers the rate limit pressure; anonymous works for most accounts
    instagram_session_user: str | None = None
    refresh_minutes: int = 60
    max_posts_per_feed: int = 30


@lru_cache
def settings() -> Settings:
    return Settings()
