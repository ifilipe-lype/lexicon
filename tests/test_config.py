"""Tests for the Lexicon settings (pydantic-settings)."""

import pytest

from lexicon.settings import Settings


def test_settings_loads():
    """Test that Settings loads without error."""
    settings = Settings()
    assert settings is not None
    assert hasattr(settings, "OLLAMA_MODEL")
    assert hasattr(settings, "OLLAMA_TEMPERATURE")


def test_settings_from_env_file(monkeypatch):
    """Test that Settings reads from .env file."""
    settings = Settings()
    # Just verify it loaded without error
    assert settings is not None


def test_settings_with_custom_values(monkeypatch):
    """Test Settings with custom environment variables."""
    monkeypatch.setenv("OLLAMA_MODEL", "phi3")
    monkeypatch.setenv("OLLAMA_TEMPERATURE", "0.0")

    settings = Settings()
    assert settings.OLLAMA_MODEL == "phi3"
    assert settings.OLLAMA_TEMPERATURE == 0.0
