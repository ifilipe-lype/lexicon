from abc import ABC, abstractmethod
from typing import TypeVar


TInput = TypeVar("TInput")
TOuput = TypeVar("TOuput")

class LLMProvider(ABC):
    @abstractmethod
    def invoke(self, input_data: TInput) -> TOuput:
        pass
