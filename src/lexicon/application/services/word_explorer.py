"""Application service for word exploration."""

from lexicon.domain.models.word import WordInput, WordDefinition, OllamaConfig
from lexicon.infrastructure.services.ollama_client import get_word_examples


def explore_word(word: str) -> WordDefinition:
    input_data = WordInput(word=word)
    config = OllamaConfig()
    return get_word_examples(input_data, config)
