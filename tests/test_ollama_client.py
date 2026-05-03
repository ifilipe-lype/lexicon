"""Tests for the Ollama infrastructure client."""

import json
from unittest.mock import patch, MagicMock
from lexicon.domain.models.word import WordInput, WordDefinition, OllamaConfig


def test_clean_json_response_json_block():
    from lexicon.infrastructure.services.ollama_client import clean_json_response

    raw = '```json\n{"definition": "test", "examples": ["a", "b", "c"]}\n```'
    result = clean_json_response(raw)
    assert result == '{"definition": "test", "examples": ["a", "b", "c"]}'


def test_clean_json_response_generic_block():
    from lexicon.infrastructure.services.ollama_client import clean_json_response

    raw = '```\n{"definition": "test", "examples": ["a", "b", "c"]}\n```'
    result = clean_json_response(raw)
    assert result == '{"definition": "test", "examples": ["a", "b", "c"]}'


def test_clean_json_response_no_block():
    from lexicon.infrastructure.services.ollama_client import clean_json_response

    raw = '{"definition": "test", "examples": ["a", "b", "c"]}'
    result = clean_json_response(raw)
    assert result == raw


@patch("lexicon.infrastructure.services.ollama_client.ollama")
def test_get_word_examples_success(mock_ollama):
    mock_response = {"message": {"content": json.dumps({
        "definition": "A brief and transient event.",
        "examples": [
            "The ephemeral nature of the moment was not lost on him.",
            "Art captures ephemeral emotions.",
            "Ephemeral trends come and go quickly.",
        ],
    })}}
    mock_ollama.chat.return_value = mock_response

    from lexicon.infrastructure.services.ollama_client import get_word_examples

    input_data = WordInput(word="ephemeral")
    config = OllamaConfig()
    result = get_word_examples(input_data, config)

    assert isinstance(result, WordDefinition)
    assert "transient" in result.definition.lower()
    assert len(result.examples) == 3
    mock_ollama.chat.assert_called_once_with(
        model=config.model_name,
        messages=[{"role": "user", "content": mock_ollama.chat.call_args[1]["messages"][0]["content"]}],
        options={"timeout": config.timeout_sec},
    )


@patch("lexicon.infrastructure.services.ollama_client.ollama")
def test_get_word_examples_json_error(mock_ollama):
    mock_ollama.chat.return_value = {"message": {"content": "not valid json"}}

    from lexicon.infrastructure.services.ollama_client import get_word_examples

    input_data = WordInput(word="test")
    config = OllamaConfig()

    import pytest
    with pytest.raises(RuntimeError, match="Failed to parse LLM JSON output"):
        get_word_examples(input_data, config)
