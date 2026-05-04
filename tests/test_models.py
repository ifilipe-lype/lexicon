"""Tests for domain models."""

from lexicon.domain.word import WordInput, WordDefinition
from pydantic import ValidationError


def test_word_input_valid():
    w = WordInput(word="ephemeral")
    assert w.word == "ephemeral"


def test_word_input_too_short():
    try:
        WordInput(word="ab")
        assert False  # Should not reach here
    except ValidationError as e:
        assert "3 characters" in str(e)


def test_word_input_exact_minimum():
    w = WordInput(word="abc")
    assert w.word == "abc"


def test_word_definition_valid():
    wd = WordDefinition(
        definition="A lasting concept.",
        examples=["One.", "Two.", "Three."],
    )
    assert wd.definition == "A lasting concept."
    assert len(wd.examples) == 3


def test_word_definition_too_few_examples():
    try:
        WordDefinition(
            definition="A lasting concept.",
            examples=["One."],
        )
        assert False  # Should not reach here
    except ValidationError as e:
        assert "three example sentences" in str(e)


def test_word_definition_truncates_extra_examples():
    wd = WordDefinition(
        definition="A lasting concept.",
        examples=["One.", "Two.", "Three.", "Four.", "Five."],
    )
    assert len(wd.examples) == 3
