# Lexicon - Word Explorer API

A word definition and example explorer powered by Ollama LLM with a FastAPI backend and web interface.

## Features

- **HTTP API**: RESTful endpoints for word lookups
- **Web UI**: Clean, responsive interface for exploring word definitions
- **LLM-Powered**: Uses Ollama with structured JSON responses
- **Validation**: Pydantic models ensure data integrity

## Quick Start

### Prerequisites

- Python 3.8+
- Ollama running locally (default: `http://localhost:11434`)
- Phi3 model pulled (`ollama pull phi3`)

### Installation

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
python -m uvicorn api.main:app --reload
```

Server starts at `http://localhost:8000`

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
pytest tests/test_api.py -v
```

### Project Structure

```
lexicon/
├── api/
│   ├── __init__.py
│   └── main.py          # FastAPI application
├── static/
│   └── frontend/
│       └── index.html   # Web UI
├── tests/
│   └── test_api.py     # API tests
├── word_explorer.py    # Core logic & LLM integration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Configuration

Edit `OllamaConfig` in `word_explorer.py` to change:
- `host`: Ollama server URL
- `model_name`: LLM model (default: "phi3")
- `timeout_sec`: Request timeout (default: 30s)
