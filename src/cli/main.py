"""CLI for Lexicon Word Explorer."""

import argparse
import sys

from pydantic import ValidationError
from lexicon.domain.word import WordInput
from lexicon.application.usecases.explore_word_usecase import ExploreWordUseCase
from lexicon.infrastructure.inference.ollama_local_provider import OllamaLocalProvider


def main() -> None:
    parser = argparse.ArgumentParser(description="Lookup word definition and examples")
    parser.add_argument("word", help="Word to look up (min 3 characters)")
    args = parser.parse_args()

    try:
        _ = WordInput(word=args.word)
    except ValidationError as ve:
        print(f"Input validation error: {ve}", file=sys.stderr)
        sys.exit(1)

    try:
        provider = OllamaLocalProvider()
        use_case = ExploreWordUseCase(llm_provider=provider)
        result = use_case.execute(args.word)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"\nWord: {args.word}")
    print("=" * 60)
    print(f"Definition:\n{result.definition}")
    print("\nExamples:")
    for i, example in enumerate(result.examples, 1):
        print(f"  {i}. {example}")
    print("=" * 60)


if __name__ == "__main__":
    main()
