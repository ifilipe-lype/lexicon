"""Tests for the CLI module."""

from unittest.mock import patch, MagicMock
from lexicon.domain.models.word import WordDefinition


@patch("lexicon.application.services.word_explorer.explore_word")
def test_cli_prints_word_definition(mock_explore):
    mock_explore.return_value = WordDefinition(
        definition="A short-lived phenomenon.",
        examples=[
            "The ephemeral beauty of the sunset amazed her.",
            "Ephemeral art installations challenge traditional notions of permanence.",
            "Social media trends are often ephemeral.",
        ],
    )

    from cli.main import main

    # Directly invoke main with mocked argv
    import sys
    original_argv = sys.argv
    sys.argv = ["lexicon-cli", "ephemeral"]
    try:
        main()
    except SystemExit as e:
        assert e.code == 0
    finally:
        sys.argv = original_argv


@patch("lexicon.application.services.word_explorer.explore_word")
def test_cli_word_too_short(mock_explore):
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


@patch("lexicon.application.services.word_explorer.explore_word")
def test_cli_handles_error(mock_explore):
    mock_explore.side_effect = RuntimeError("Ollama connection failed")

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
