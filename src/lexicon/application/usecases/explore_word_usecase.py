"""Application usecase for word exploration."""

from lexicon.domain.word import WordInput, WordDefinition
from lexicon.application.providers.llm_provider import LLMProvider


class ExploreWordUseCase:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def execute(self, word: str) -> WordDefinition:
        """Explore a word using the provided LLM provider.

        Args:
            word: The word to explore (must be at least 3 characters).

        Returns:
            WordDefinition with definition and examples.
        """

        input_data = WordInput(word=word)

        return self.llm_provider.invoke(input_data)
