"""Generic LangChain LLM provider that works with any LangChain chat model."""

from typing import Generic, cast

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.language_models.chat_models import BaseChatModel

from lexicon.application.providers.llm_provider import LLMProvider, LLMInvokeInput, TPayload, TOutput


class LangChainProvider(LLMProvider, Generic[TPayload, TOutput]):
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def invoke(self, input_data: LLMInvokeInput[TPayload, TOutput]) -> TOutput:
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("user", input_data.prompt)
            ])
            output_parser = PydanticOutputParser(pydantic_object=input_data.output_model)
            chain = prompt | self.llm | output_parser
            
            result = chain.invoke(input_data.payload)
            
            return cast(TOutput, result)
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")
