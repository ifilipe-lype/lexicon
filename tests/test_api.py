import pytest
from fastapi.testclient import TestClient
from src.http.app import app

client = TestClient(app)

def test_search_word_invalid_length():
    response = client.get("/search?word=ab")
    assert response.status_code == 400

def test_search_word_missing_parameter():
    response = client.get("/search")
    assert response.status_code == 422

def test_frontend_serves_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
