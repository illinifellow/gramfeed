from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GRAMFEED_", env_file=".env")

    database_url: str = "postgresql+asyncpg://gramfeed:gramfeed@localhost/gramfeed"
    redis_url: str = "redis://localhost:6379/0"
    public_url: str = "http://localhost:8000"
    admin_token: str = "change-me"
    # media is re-hosted: Instagram CDN links expire within hours, feed readers fetch days later