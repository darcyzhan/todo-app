from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "TodoMaster Pro"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite+aiosqlite:///./todomaster.db"
    DATABASE_ECHO: bool = False

    SECRET_KEY: str = "todomaster-super-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    WECHAT_APP_ID: str = ""
    WECHAT_APP_SECRET: str = ""

    REDIS_URL: Optional[str] = None
    MEILISEARCH_URL: Optional[str] = None
    MEILISEARCH_KEY: Optional[str] = None

    COS_SECRET_ID: Optional[str] = None
    COS_SECRET_KEY: Optional[str] = None
    COS_BUCKET: Optional[str] = None
    COS_REGION: Optional[str] = None

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
