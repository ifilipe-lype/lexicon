from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from word_explorer import WordInput, WordDefinition, OllamaConfig, get_word_examples, clean_json_response
import json, os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend at root
@app.get("/")
async def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), "../static/frontend/index.html")
    return FileResponse(frontend_path)

@app.get("/search")
async def search_word(word: str = Query(..., description="Word to search (minimum 3 characters)")):
    if len(word) < 3:
        raise HTTPException(status_code=400, detail="Word must be at least 3 characters")

    try:
        config = OllamaConfig()
        result = get_word_examples(WordInput(word=word), config)
        return {
            "definition": result.definition,
            "examples": result.examples
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)