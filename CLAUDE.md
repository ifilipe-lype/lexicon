# CLAUDE.md – Lexicon Project

**Project:** Lexicon – LLM-Agnostic Word Explorer

**Purpose:** Provide a FastAPI backend and web UI for exploring word definitions and example sentences powered by LLMs through a provider abstraction (Ollama, OpenAI, Anthropic, etc.).

---

## Core Details
- **API Endpoint**: `GET /search?word=<term>` – returns a JSON object with `definition` and `examples`.
- **Web UI**: Served at `/` from `src/lexicon/infrastructure/web/static/index.html`.
- **LLM Integration**: Provider pattern in `src/lexicon/infrastructure/inference/` with LangChain.
- **Configuration**: `src/lexicon/settings.py` using pydantic-settings (env vars supported).
- **CLI**: Run `poetry run lexicon-cli` for command-line usage.
- **Testing**: Run `pytest tests/ -v`.

---

## Architecture
```
src/lexicon/
├── domain/              # Domain models (WordInput, WordDefinition)
├── application/         # Use cases and providers
│   ├── prompts/        # Prompt templates
│   └── providers/      # LLM provider interface
├── infrastructure/      # External adapters
│   ├── inference/      # LangChain providers (Ollama, etc.)
│   └── web/           # Static files and web UI
└── settings.py         # Configuration
```

## Development Guidelines
- **Layered architecture**: Domain → Application → Infrastructure
- **Provider pattern**: Add new LLM support via `LLMProvider` interface
- **FastAPI routes**: Defined in `src/http/app.py`
- **Pydantic models**: Used for validation in `src/lexicon/domain/word.py`
- **Run dev server**: `poetry run web-dev` or `uvicorn src.http.app:app --reload`

---

## Token‑Optimization (RTK) Hook
The Claude Code hook automatically rewrites CLI commands to route through **RTK** for token savings.  Typical usage:
```
rtk gain            # Show token savings analytics
rtk discover        # Find missed optimization opportunities
rtk proxy <cmd>     # Run a raw command unchanged (debugging)
```
All standard commands (e.g., `git status`, `pytest`) are transparently proxied via `rtk`.

> **Note:** If `rtk gain` fails, verify you are not colliding with the `reachingforthejack/rtk` package.

---

## Contribution Rules
1. **Do not commit secrets** – `.gitignore` already excludes `.env` and other sensitive files.
2. **All new code must be covered by tests** (unit or integration) before merging.
3. **Maintain API stability** – keep response schema identical; deprecate via versioned routes if needed.
4. **Use the RTK hook** for all command‑line operations to reduce Claude token usage.
5. **Follow existing linting/formatting** – `black` and `ruff` are configured via `pyproject.toml`.
6. **Never commit or push changes unless explicitly asked** – wait for user instruction before git commit/push.

---

## Reference Files
- `src/http/app.py` – FastAPI application and route definitions.
- `src/lexicon/domain/word.py` – Domain models.
- `src/lexicon/application/usecases/explore_word_usecase.py` – Business logic.
- `src/lexicon/infrastructure/inference/langchain_provider.py` – LangChain integration.
- `src/lexicon/settings.py` – Configuration settings.
- `tests/` – All tests (API, CLI, domain, infrastructure).

---

## Dependencies
Managed via Poetry (`pyproject.toml`):
- `fastapi`, `uvicorn` – Web framework
- `langchain-core`, `langchain-ollama` – LLM integration
- `pydantic`, `pydantic-settings` – Data validation and configuration

---

## Global Settings Reference
@RTK.md
