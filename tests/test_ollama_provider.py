"""Tests for the OllamaLocalProvider with LangChain."""

from unittest.mock import patch, MagicMock

from lexicon.domain.word import WordInput, WordDefinition
from lexicon.infrastructure.inference.ollama_local_provider import (
    OllamaLocalProvider,
)


def test_ollama_provider_generate_word_definition():
    expected = WordDefinition(
        definition="A brief and transient event.",
        examples=[
            "The ephemeral nature of the moment was not lost on him.",
            "Art captures ephemeral emotions.",
            "Ephemeral trends come and go quickly.",
        ],
    )

    with patch("langchain_ollama.ChatOllama") as MockChatOllama:
        # Create provider (will use mocked ChatOllama)
        provider = OllamaLocalProvider()

        # Now mock the chain to return the expected result directly
        provider.chain = MagicMock()
        provider.chain.invoke.return_value = expected

        input_data = WordInput(word="ephemeral")
        result = provider.invoke(input_data)

        assert isinstance(result, WordDefinition)
        assert "transient" in result.definition.lower()
        assert len(result.examples) == 3


def test_ollama_provider_error_handling():
    with patch("langchain_ollama.ChatOllama") as MockChatOllama:
        provider = OllamaLocalProvider()

        # Mock chain to raise an error
        provider.chain = MagicMock()
        provider.chain.invoke.side_effect = RuntimeError("Connection refused")

        input_data = WordInput(word="test")

        import pytest
        with pytest.raises(RuntimeError, match="LLM generation failed"):
            provider.invoke(input_data)

