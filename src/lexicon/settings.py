"""Configuration for LLM providers using BaseConfig class hierarchy with pydantic-settings."""
from logging import getLogger
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


logger = getLogger(__name__)


class Settings(BaseSettings):
    """Typed settings for the Lexicon package, auto-loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "gpt-4")
    OLLAMA_TEMPERATURE: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
    OLLAMA_MAX_TOKENS: int = int(os.getenv("OLLAMA_MAX_TOKENS", "2048"))
    OLLAMA_VERBOSE: bool = os.getenv("OLLAMA_VERBOSE", "false").lower() in ("true", "1", "yes")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "")

    @classmethod
    def load_settings(cls) -> "Settings":
        """
        Load settings from environment variables, ensuring .env file exists.
        """
        assert os.path.exists(".env"), "No .env file found. Please create one with the necessary environment variables."

        return Settings()


settings = Settings.load_settings()
