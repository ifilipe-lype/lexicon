"""FastAPI entry point for the Lexicon Word Explorer.

Provides a `/search` endpoint that returns a word definition and three example
sentences. The handler delegates to the application service, keeping the web
layer thin and testable.
"""
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from lexicon.application.services.word_explorer import explore_word

app = FastAPI(title="Lexicon Word Explorer API")

# Serve static UI from '/static' (does not shadow API routes)
static_dir = os.path.join(os.path.dirname(__file__), 'static', 'frontend')
if os.path.exists(static_dir):
    app.mount("/home", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/search")
async def search(word: str = Query(..., description="Word to search (minimum 3 characters)")):
    if len(word) < 3:
        raise HTTPException(status_code=400, detail="Word must be at least 3 characters long")
    try:
        result = explore_word(word)
        return {"definition": result.definition, "examples": result.examples}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/")
async def root():
    return RedirectResponse(url="/home")
