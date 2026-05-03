# CLAUDE.md – Lexicon Project

**Project:** Lexicon – Word Explorer API

**Purpose:** Provide a FastAPI backend and web UI for exploring word definitions and example sentences powered by an Ollama LLM.

---

## Core Details
- **API Endpoint**: `GET /search?word=<term>` – returns a JSON object with `definition` and `examples`.
- **Web UI**: Served at `/` from `static/frontend/index.html`.
- **LLM Integration**: Implemented in `word_explorer.py` using Ollama (`phi3` model by default).
- **Configuration**: Adjust `OllamaConfig` in `word_explorer.py` for host, model, and timeout.
- **Testing**: Run `pytest tests/test_api.py -v`.

---

## Development Guidelines
- Keep FastAPI route definitions in `src/api/main.py` and static assets under `src/static/`.
- Use Pydantic models for request validation – they guarantee a minimum 3‑character `word` query.
- Ensure new endpoints follow the existing pattern: clear docstring, input validation, and proper HTTP status codes.
- Run the server with `python -m uvicorn api.main:app --reload` during development.

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

---

## Reference Files
- `src/api/main.py` – FastAPI application and route definitions.
- `src/word_explorer.py` – Core LLM interaction logic.
- `src/static/frontend/index.html` – Web UI.
- `requirements.txt` – Python dependencies.

---

## Global Settings Reference
@RTK.md
