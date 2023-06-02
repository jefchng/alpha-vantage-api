from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    alpha_vantage_api_key: str

    class Config:
        env_file = ".env"
        secrets_dir = "/run/secrets"


@lru_cache()
def get_settings():
    return Settings()
