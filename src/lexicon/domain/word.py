"""Domain models for Word Explorer."""

from pydantic import BaseModel, Field, field_validator
from typing import List


class WordInput(BaseModel):
    word: str = Field(..., description="Word to look up (min 3 chars)")

    @field_validator("word")
    def check_length(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Word must be at least 3 characters long")
        return v


class WordDefinition(BaseModel):
    definition: str = Field(..., description="One-paragraph definition")
    examples: List[str] = Field(..., description="Exactly three example sentences")

    @field_validator("examples")
    def check_example_count(cls, v: List[str]) -> List[str]:
        if len(v) < 3:
            raise ValueError("At least three example sentences required")
        return v[:3]
