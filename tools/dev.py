"""Development server entry point."""

import uvicorn


def main() -> None:
    """Run the FastAPI app with auto‑reload."""
    uvicorn.run("src.http.app:app", host="0.0.0.0", port=8000, reload=True)
