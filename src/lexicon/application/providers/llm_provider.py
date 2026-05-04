from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

TPayload = TypeVar("TPayload")
TOutput = TypeVar("TOutput")


class LLMInvokeInput(BaseModel, Generic[TPayload, TOutput]):
    prompt: str
    payload: TPayload
    output_model: type[TOutput]


class LLMProvider(ABC, Generic[TPayload, TOutput]):
    @abstractmethod
    def invoke(self, input_data: LLMInvokeInput[TPayload, TOutput]) -> TOutput:
        pass
