"""FastAPI entry point for the Lexicon Word Explorer.

Provides a `/search` endpoint that returns a word definition and three example
sentences. The handler delegates to the application service, keeping the web
layer thin and testable.
"""
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from lexicon.application.usecases.explore_word_usecase import ExploreWordUseCase
from lexicon.infrastructure.inference.ollama_local_provider import OllamaLocalProvider

app = FastAPI(title="Lexicon Word Explorer API")

# Create the LLM provider based on configuration (env vars)
ollama_provider = OllamaLocalProvider()

# Serve static UI from '/static' (does not shadow API routes)
static_dir = os.path.join(os.path.dirname(__file__), 'static', 'frontend')
if os.path.exists(static_dir):
    app.mount("/home", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/search")
async def search(word: str = Query(..., description="Word to search (minimum 3 characters)")):
    try:
        use_case = ExploreWordUseCase(llm_provider=ollama_provider)
        result = use_case.execute(word)
        return {"definition": result.definition, "examples": result.examples}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/")
async def root():
    return RedirectResponse(url="/home")
