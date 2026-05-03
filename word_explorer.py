import argparse
import json
import ollama
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List

# ==============================
# VALIDATION MODELS
# ==============================
class WordInput(BaseModel):
    word: str = Field(..., description="The word to look up (minimum 3 characters)")

    @field_validator("word")
    def check_length(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Word must be at least 3 characters long")
        return v

class OllamaConfig(BaseModel):
    host: str = "http://localhost:11434"
    model_name: str = "phi3"
    timeout_sec: int = 30

def clean_json_response(raw: str) -> str:
    """Strip markdown code fences from LLM response."""
    cleaned = raw.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()

# ==============================
# CORE FUNCTIONALITY
# ==============================
class WordDefinition(BaseModel):
    """Structured definition and examples returned by the LLM."""
    definition: str = Field(..., description="One‑paragraph definition of the word")
    examples: List[str] = Field(..., description="A list of exactly three example sentences")

    @field_validator("examples")
    def check_example_count(cls, v: List[str]) -> List[str]:
        if len(v) < 3:
            raise ValueError("At least three example sentences are required")
        return v[:3]  # keep only first three

def get_word_examples(input_data: WordInput, config: OllamaConfig) -> WordDefinition:
    """Generate a structured definition and usage examples via Ollama.

    The LLM is prompted to return JSON matching the WordDefinition schema.
    """
    prompt = f"Generate detailed information about the word {input_data.word}:\n\n"
    prompt += "Return a JSON object with these keys:\n"
    prompt += "- \"definition\": a concise one‑paragraph definition.\n"
    prompt += "- \"examples\": an array of exactly three example sentences, each starting with a capital letter and ending with a period.\n\n"
    prompt += "Example response:\n"
    prompt += "{\n  \"definition\": \"...\",\n  \"examples\": [\"...\", \"...\", \"...\"]\n}\n"

    raw = ""
    try:
        response = ollama.chat(
            model=config.model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"timeout": config.timeout_sec},
        )
        raw = response["message"]["content"]
        cleaned = clean_json_response(raw)
        data = json.loads(cleaned)
        return WordDefinition.model_validate(data)
    except json.JSONDecodeError as je:
        raise RuntimeError(f"Failed to parse LLM JSON output: {je}\nRaw output: {raw}")
    except Exception as e:
        raise RuntimeError(f"LLM generation failed: {e}")

# ==============================
# CLI INTERFACE
# ==============================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI for getting word definitions and examples via Ollama",
        usage="python word_explorer.py <word>",
    )
    parser.add_argument(
        "word",
        type=str,
        help="The word to look up (minimum 3 characters)",
    )
    args = parser.parse_args()

    # Validate input
    try:
        validated_input = WordInput(word=args.word)
    except ValidationError as ve:
        print(f"Input validation error: {ve}")
        exit(1)

    config = OllamaConfig()
    try:
        result = get_word_examples(validated_input, config)
        print(f"\nWord: {validated_input.word}")
        print("=" * 60)
        print(f"Definition:\n{result.definition}")
        print("\nExamples:")
        for i, example in enumerate(result.examples, 1):
            print(f"  {i}. {example}")
        print("=" * 60)
    except Exception as e:
        print(f"Error generating response: {e}")
        exit(1)
