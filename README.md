# Lexicon - Word Explorer

A word definition and example explorer with a FastAPI backend, web interface, and CLI — powered by LLMs through a provider abstraction (Ollama, OpenAI, Anthropic, etc.).

## Features

- **HTTP API**: RESTful endpoints for word lookups
- **Web UI**: Clean, responsive interface for exploring word definitions
- **CLI**: Command-line interface for quick lookups
- **LLM-Agnostic**: Provider pattern supports multiple LLM backends via LangChain
- **Validation**: Pydantic models ensure data integrity
- **Configuration**: Environment-based config with pydantic-settings

## Quick Start

### Prerequisites

- Python 3.9+
- Poetry (dependency management)
- Ollama running locally (default: `http://localhost:11434`) or other supported LLM

### Installation

```bash
poetry install
```

### Running the Server

```bash
poetry run web-dev
```

Or manually with uvicorn:

```bash
uvicorn src.http.app:app --reload
```

Server starts at `http://localhost:8000`

### CLI Usage

```bash
poetry run lexicon-cli search "ephemeral"
```

## API Documentation

### GET /search

Search for a word's definition and examples.

**Parameters:**
- `word` (query, required): The word to look up (minimum 3 characters)

**Response:**
```json
{
  "definition": "A detailed one-paragraph definition...",
  "examples": [
    "First example sentence.",
    "Second example sentence.",
    "Third example sentence."
  ]
}
```

**Error Responses:**
- `400`: Word must be at least 3 characters
- `422`: Missing or invalid parameters
- `500`: Processing error (LLM unavailable, etc.)

### GET /

Serves the web interface (`index.html`)

## Web Interface

Visit `http://localhost:8000` in your browser to use the interactive UI:
- Enter a word (3+ characters)
- Click "Search" or press Enter
- View the definition and examples

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Project Structure

```
lexicon/
├── src/
│   ├── lexicon/              # Core package
│   │   ├── domain/          # Domain models (WordInput, WordDefinition)
│   │   ├── application/     # Use cases and providers
│   │   │   ├── prompts/    # Prompt templates
│   │   │   └── providers/  # LLM provider interface
│   │   ├── infrastructure/ # External adapters
│   │   │   ├── inference/  # LangChain providers
│   │   │   └── web/        # Static files
│   │   └── settings.py     # Configuration
│   ├── http/               # FastAPI application
│   ├── cli/                # CLI entry point
│   └── static/             # Static assets
├── tests/                   # All tests
├── pyproject.toml          # Poetry dependencies
└── README.md              # This file
```

### Configuration

Configuration is managed via `src/lexicon/settings.py` using pydantic-settings.

Environment variables (optional):
- `OLLAMA_MODEL` – LLM model (default: "phi3")
- `OLLAMA_HOST` – Ollama server URL (default: "http://localhost:11434")
- `OLLAMA_TEMPERATURE` – Temperature setting (default: 0.0)
- `OLLAMA_VERBOSE` – Verbose output (default: false)

### Adding a New LLM Provider

1. Create a new provider class implementing `LLMProvider` interface
2. Use LangChain integrations or implement directly
3. Update configuration in `settings.py` if needed
