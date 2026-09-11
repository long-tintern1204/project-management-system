from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = Field(default="sqlite:///./app.db")
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def _secret_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("JWT_SECRET_KEY が設定されていません。.env を確認してください。")
        return v

    @field_validator("JWT_EXPIRE_MINUTES")
    @classmethod
    def _expire_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("JWT_EXPIRE_MINUTES は 1 以上を指定してください。")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
