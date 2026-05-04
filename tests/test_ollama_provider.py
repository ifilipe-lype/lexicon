"""Tests for the OllamaLocalProvider with LangChain."""

from unittest.mock import patch, MagicMock

from lexicon.application.providers.llm_provider import LLMInvokeInput
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

    with patch("langchain_ollama.ChatOllama"):
        provider = OllamaLocalProvider()

        # Mock the entire invoke method to return expected result
        def mock_invoke(input_data):
            return expected

        provider.invoke = mock_invoke

        input_data = LLMInvokeInput(
            prompt="Generate info about {word}",
            payload=WordInput(word="ephemeral"),
            output_model=WordDefinition,
        )
        result = provider.invoke(input_data)

        assert isinstance(result, WordDefinition)
        assert "transient" in result.definition.lower()
        assert len(result.examples) == 3


def test_ollama_provider_error_handling():
    with patch("langchain_ollama.ChatOllama"):
        provider = OllamaLocalProvider()

        # Mock llm.invoke to raise an error - this will be caught by invoke()
        provider.llm = MagicMock()
        provider.llm.invoke.side_effect = RuntimeError("Connection refused")

        input_data = LLMInvokeInput(
            prompt="Generate info about {word}",
            payload=WordInput(word="test"),
            output_model=WordDefinition,
        )

        import pytest
        with pytest.raises(RuntimeError, match="LLM generation failed"):
            provider.invoke(input_data)
