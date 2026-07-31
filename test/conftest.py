import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    test_client = TestClient(app)
    yield test_client

@pytest.fixture
def mock_is_blocked_domain():
    with patch("app.url_validator.is_blocked_domain") as mock_func:
        mock_func.return_value = False

        yield mock_func
