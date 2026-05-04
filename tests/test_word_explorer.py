"""Tests for the ExploreWordUseCase."""

from typing import cast
from unittest.mock import MagicMock

from lexicon.domain.word import WordDefinition
from lexicon.application.providers.llm_provider import LLMProvider, LLMInvokeInput


def test_explore_word_calls_provider():
    mock_provider = MagicMock(spec=LLMProvider)
    mock_provider.invoke.return_value = WordDefinition(
        definition="A feeling of great pleasure or happiness.",
        examples=[
            "She felt immense joy when she heard the news.",
            "The team celebrated with joy after winning the championship.",
            "Simple moments often bring the most joy.",
        ],
    )

    from lexicon.application.usecases.explore_word_usecase import ExploreWordUseCase

    use_case = ExploreWordUseCase(llm_provider=mock_provider)
    result = use_case.execute("joy")

    assert isinstance(result, WordDefinition)
    assert len(result.examples) == 3
    mock_provider.invoke.assert_called_once()
    call_args = mock_provider.invoke.call_args
    assert isinstance(call_args[0][0], LLMInvokeInput)
    assert call_args[0][0].payload.word == "joy"


def test_explore_word_requires_provider():
    """Test that ExploreWordUseCase requires a provider."""
    from lexicon.application.usecases.explore_word_usecase import ExploreWordUseCase

    try:
        ExploreWordUseCase(llm_provider=cast(LLMProvider, None))
        assert False, "Should have raised"
    except Exception:
        pass  # Expected
