from uuid import uuid4

from fastapi.testclient import TestClient

def get_fresh_conversation_id() -> str:
    return str(uuid4())


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


def test_chat_retains_conversation_history(client: TestClient) -> None:
    conversation_id = get_fresh_conversation_id()

    payload = {"query": "my favorite color is indigo", "conversation_id": conversation_id}
    headers = {"Content-Type": "application/json"}
    _ = client.post("/chat", json=payload, headers=headers)

    payload = {"query": "whats my favorite color", "conversation_id": conversation_id}
    headers = {"Content-Type": "application/json"}
    response = client.post("/chat", json=payload, headers=headers)
    response_json = response.json()

    assert "content" in response_json
    assert "indigo" in response_json["content"].lower()


def test_chat_doesnt_have_history_of_unrelated_conversations(client: TestClient) -> None:
    payload = {"query": "whats my favorite color", "conversation_id": get_fresh_conversation_id()}
    headers = {"Content-Type": "application/json"}
    response = client.post("/chat", json=payload, headers=headers)
    response_json = response.json()

    assert "content" in response_json
    assert "indigo" not in response_json["content"].lower()
