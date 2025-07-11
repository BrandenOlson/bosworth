
from fastapi.testclient import TestClient
import pytest

def test_ping(client: TestClient) -> None:
    result = client.get("/ping")
    result_json = result.json()

    assert "Hello" in result_json
    assert result_json["Hello"] == "World"
