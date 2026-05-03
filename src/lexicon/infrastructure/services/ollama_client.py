"""Infrastructure adapter for Ollama LLM."""

import json
import ollama
from lexicon.domain.models.word import WordInput, WordDefinition, OllamaConfig


def clean_json_response(raw: str) -> str:
    cleaned = raw.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()


def get_word_examples(input_data: WordInput, config: OllamaConfig) -> WordDefinition:
    prompt = (
        f"Generate detailed information about the word {input_data.word}:\n\n"
        "Return a JSON object with these keys:\n"
        "- \"definition\": a concise one‑paragraph definition.\n"
        "- \"examples\": an array of exactly three example sentences, each starting with a capital letter and ending with a period.\n\n"
        "Example response:\n"
        "{\n  \"definition\": \"...\",\n  \"examples\": [\"...\", \"...\", \"...\"]\n}\n"
    )

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
