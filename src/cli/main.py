"""CLI for Lexicon Word Explorer."""

import argparse
import sys

from lexicon.application.services.word_explorer import explore_word
from lexicon.domain.models.word import WordInput
from pydantic import ValidationError


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
        result = explore_word(args.word)
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
