import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.routes import redirect_cache
from app.token_gen import generate_token


def test_redirect_cache_hit(client):
    redirect_cache["test"] = "http://example.com"
    response = client.get("/r/test", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "http://example.com"

def test_redirect_not_found(client):
    response = client.get("/r/not_exist")
    assert response.status_code == 404

def test_token_generate_success():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    url = "http://example.com/mock_test"
    token = generate_token(url, mock_db)

    assert isinstance(token, str)
    assert len(token) == 7

def test_token_generate_retry(mocker):
    mock_db = MagicMock()

    mock_exist = mocker.patch("app.token_gen.token_exists_in_db")
    mock_exist.side_effect = [True, True, False]

    url = "https://google.com"
    token = generate_token(url, mock_db)

    assert len(token) == 7
    assert mock_exist.call_count == 3

def test_token_generate_failed(mocker):
    mock_db = MagicMock()

    mock_exist = mocker.patch("app.token_gen.token_exists_in_db", return_value=True)

    url = "https://google.com"
    with pytest.raises(RuntimeError) as execute_info:
        generate_token(url, mock_db)

    assert "All retries are exhausted.." in str(execute_info.value)
    assert mock_exist.call_count == 10



