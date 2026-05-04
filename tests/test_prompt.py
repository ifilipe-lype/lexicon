"""Tests for prompt templates."""

from lexicon.application.prompts.word_prompt import build_word_prompt


def test_build_word_prompt():
    prompt = build_word_prompt("ephemeral")
    assert "ephemeral" in prompt
    assert "definition" in prompt
    assert "examples" in prompt
    assert "JSON" in prompt


def test_build_word_prompt_different_words():
    words = ["ephemeral", "serendipity", "quintessential"]
    for word in words:
        prompt = build_word_prompt(word)
        assert word in prompt
