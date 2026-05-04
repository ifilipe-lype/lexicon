"""Application usecase for word exploration."""

from lexicon.domain.word import WordInput, WordDefinition
from lexicon.application.providers.llm_provider import LLMProvider, LLMInvokeInput
from lexicon.application.prompts.word_prompt import build_word_prompt


class ExploreWordUseCase:
    def __init__(self, llm_provider: LLMProvider[WordInput, WordDefinition]):
        self.llm_provider = llm_provider
        

    def execute(self, word: str) -> WordDefinition:
        """Explore a word using the provided LLM provider.

        Args:
            word: The word to explore (must be at least 3 characters).

        Returns:
            WordDefinition with definition and examples.
        """

        input_data = LLMInvokeInput(
            prompt=build_word_prompt("{word}"),
            payload=WordInput(word=word),
            output_model=WordDefinition,
        )

        return self.llm_provider.invoke(input_data)
