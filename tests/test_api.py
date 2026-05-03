import pytest
from fastapi.testclient import TestClient
from api.main import app
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio

client = TestClient(app)

@pytest.fixture
def mock_ollama_config():
    """Mock OllamaConfig to simulate API responses"""
    from word_explorer import OllamaConfig
    class MockOllamaConfig(OllamaConfig):
        def __init__(self):
            self.model_name = "phi3"
            self.timeout_sec = 1
    return MockOllamaConfig()

def test_search_word_success(mock_ollama_config):
    """Test successful word search returns 200 and expected structure"""
    with client:
        response = client.get("/search?word=example")
        assert response.status_code == 200
        data = response.json()
        assert "definition" in data
        assert "examples" in data
        assert isinstance(data["examples"], list)
        assert len(data["examples"]) == 3

def test_search_word_invalid_length():
    """Test invalid word length returns 400 error"""
    response = client.get("/search?word=ab")
    assert response.status_code == 400
    assert "Word must be at least 3 characters" in response.json()["detail"]

def test_search_word_missing_parameter():
    """Test missing query parameter returns 422"""
    response = client.get("/search")
    assert response.status_code == 422

def test_frontend_serves_index():
    """Test that frontend serves index.html"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Word Explorer" in response.text

def test_api_error_handling(monkeypatch):
    """Test error handling in API"""
    def mock_get_word_examples(*args, **kwargs):
        raise RuntimeError("Test error")

    monkeypatch.setattr("word_explorer.get_word_examples", mock_get_word_examples)

    response = client.get("/search?word=test")
    assert response.status_code == 500
    assert "Processing error" in response.json()["detail"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])