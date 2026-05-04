"""Ollama local LLM provider using LangChain.

This is a convenience wrapper that configures LangChain's ChatOllama
and delegates to LangChainProvider.
"""

from langchain_ollama import ChatOllama

from lexicon.infrastructure.inference.langchain_provider import LangChainProvider
from lexicon.settings import settings


class OllamaLocalProvider(LangChainProvider):
    def __init__(self, config=None):
        super().__init__(
            ChatOllama(
                model=settings.OLLAMA_MODEL,
                temperature=settings.OLLAMA_TEMPERATURE,
                verbose=settings.OLLAMA_VERBOSE,
            )
        )
