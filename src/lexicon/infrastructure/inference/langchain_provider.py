"""Generic LangChain LLM provider that works with any LangChain chat model."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from lexicon.domain.word import WordInput, WordDefinition
from lexicon.application.providers.llm_provider import LLMProvider
from lexicon.application.prompts.word_prompt import build_word_prompt


class LangChainProvider(LLMProvider):
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("user", build_word_prompt("{word}"))
        ])
        self.output_parser = PydanticOutputParser(pydantic_object=WordDefinition)
        self.chain = self.prompt | self.llm | self.output_parser

    def invoke(self, input_data: WordInput) -> WordDefinition:
        try:
            result = self.chain.invoke(input_data)
            return result
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")
