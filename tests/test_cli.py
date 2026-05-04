"""Tests for the CLI module."""

from unittest.mock import patch, MagicMock
from lexicon.domain.word import WordDefinition


@patch("lexicon.application.usecases.explore_word_usecase.ExploreWordUseCase")
def test_cli_prints_word_definition(mock_usecase_class):
    mock_instance = MagicMock()
    mock_instance.execute.return_value = WordDefinition(
        definition="A short-lived phenomenon.",
        examples=[
            "The ephemeral beauty of the sunset amazed her.",
            "Ephemeral art installations challenge traditional notions of permanence.",
            "Social media trends are often ephemeral.",
        ],
    )
    mock_usecase_class.return_value = mock_instance

    from cli.main import main

    import sys
    original_argv = sys.argv
    sys.argv = ["lexicon-cli", "ephemeral"]
    try:
        main()
    except SystemExit as e:
        assert e.code == 0
    finally:
        sys.argv = original_argv


@patch("lexicon.application.usecases.explore_word_usecase.ExploreWordUseCase")
def test_cli_word_too_short(mock_usecase_class):
    from cli.main import main

    import sys
    original_argv = sys.argv
    sys.argv = ["lexicon-cli", "ab"]
    try:
        main()
    except SystemExit as e:
        assert e.code != 0
    finally:
        sys.argv = original_argv


@patch("lexicon.application.usecases.explore_word_usecase.ExploreWordUseCase")
def test_cli_handles_error(mock_usecase_class):
    mock_instance = MagicMock()
    mock_instance.execute.side_effect = RuntimeError("Ollama connection failed")
    mock_usecase_class.return_value = mock_instance

    from cli.main import main

    import sys
    original_argv = sys.argv
    sys.argv = ["lexicon-cli", "ephemeral"]
    try:
        main()
    except SystemExit as e:
        assert e.code != 0
    finally:
        sys.argv = original_argv
