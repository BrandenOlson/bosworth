from fastapi.testclient import TestClient


def test_ping(client: TestClient) -> None:
    result = client.get("/ping")
    result_json = result.json()

    assert "ping" in result_json
    assert result_json["ping"] == "pong"


def test_chat(client: TestClient) -> None:
    payload = {"query": "what is your favorite number?"}
    headers = {"Content-Type": "application/json"}
    result = client.post("/chat", json=payload, headers=headers)
    result_json = result.json()

    assert "content" in result_json
    assert any(number in result_json["content"].lower() for number in ["13", "thirteen"])
