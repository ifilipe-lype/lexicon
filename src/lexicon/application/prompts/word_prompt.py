def build_word_prompt(word: str) -> str:
    return (
        "Generate detailed information about the word " + word + ":\n\n"
        "Return a JSON object with these keys:\n"
        '- "definition": a concise one-paragraph definition.\n'
        '- "examples": an array of exactly three example sentences, '
        "each starting with a capital letter and ending with a period.\n\n"
        "Example response:\n"
        '{{\n  "definition": "...",\n  "examples": ["...", "...", "..."]\n}}\n'
    )
