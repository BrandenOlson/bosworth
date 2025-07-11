import pytest
from fastapi.testclient import TestClient

from bosworth.app import app

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)