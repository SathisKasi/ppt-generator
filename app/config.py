from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Presentation Generator"
    max_upload_size_mb: int = 50
    upload_directory: Path = Path("uploads")
    output_directory: Path = Path("output")
    llm_base_url: str = "http://localhost:8000/v1"
    llm_api_key: str = "local"
    llm_model: str = "Qwen3-32B"
    llm_timeout_seconds: int = 90
    use_llm: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_directory.mkdir(parents=True, exist_ok=True)
    settings.output_directory.mkdir(parents=True, exist_ok=True)
    return settings