"""Tests for the word_explorer application service."""

from unittest.mock import patch, MagicMock
from lexicon.domain.models.word import WordDefinition, OllamaConfig, WordInput


@patch("lexicon.application.services.word_explorer.get_word_examples")
def test_explore_word_calls_infrastructure(mock_get_examples):
    mock_get_examples.return_value = WordDefinition(
        definition="A feeling of great pleasure or happiness.",
        examples=[
            "She felt immense joy when she heard the news.",
            "The team celebrated with joy after winning the championship.",
            "Simple moments often bring the most joy.",
        ],
    )
    from lexicon.application.services.word_explorer import explore_word

    result = explore_word("joy")

    assert isinstance(result, WordDefinition)
    assert "pleasure" in result.definition.lower() or "happiness" in result.definition.lower()
    assert len(result.examples) == 3
    mock_get_examples.assert_called_once()
    call_args = mock_get_examples.call_args
    assert isinstance(call_args[0][0], WordInput)
    assert call_args[0][0].word == "joy"
    assert isinstance(call_args[0][1], OllamaConfig)
