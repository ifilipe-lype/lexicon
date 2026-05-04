"""Tests for the FastAPI application."""

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from lexicon.domain.word import WordDefinition

import src.http.app as app_module
from src.http.app import app

client = TestClient(app, follow_redirects=False)


def make_word_definition(word="ephemeral"):
    return WordDefinition(
        definition="Lasting for a very short time.",
        examples=[
            "The ephemeral beauty of the cherry blossoms attracts visitors every spring.",
            "Fame in the digital age can be incredibly ephemeral.",
            "He lamented the ephemeral nature of human achievements.",
        ],
    )


@patch("src.http.app.ExploreWordUseCase")
def test_search_word_success(mock_usecase_class):
    mock_instance = MagicMock()
    mock_instance.execute.return_value = make_word_definition("ephemeral")
    mock_usecase_class.return_value = mock_instance

    response = client.get("/search?word=ephemeral")
    assert response.status_code == 200
    data = response.json()
    assert "definition" in data
    assert "examples" in data
    assert len(data["examples"]) == 3
    mock_instance.execute.assert_called_once_with("ephemeral")


@patch("src.http.app.ExploreWordUseCase")
def test_search_word_ollama_error(mock_usecase_class):
    mock_instance = MagicMock()
    mock_instance.execute.side_effect = ValueError("Ollama unavailable")
    mock_usecase_class.return_value = mock_instance

    response = client.get("/search?word=ephemeral")
    assert response.status_code == 400
    assert "Ollama unavailable" in response.json()["detail"]


@patch("src.http.app.ExploreWordUseCase")
def test_search_word_unexpected_error(mock_usecase_class):
    mock_instance = MagicMock()
    mock_instance.execute.side_effect = RuntimeError("Connection refused")
    mock_usecase_class.return_value = mock_instance

    response = client.get("/search?word=ephemeral")
    assert response.status_code == 500
    assert "Connection refused" in response.json()["detail"]


def test_search_word_invalid_length():
    response = client.get("/search?word=ab")
    assert response.status_code == 400
    assert "3 characters" in response.json()["detail"]


def test_search_word_missing_parameter():
    response = client.get("/search")
    assert response.status_code == 422


def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 307
    assert response.headers["location"] == "/home"


def test_static_frontend():
    response = client.get("/home", follow_redirects=True)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
