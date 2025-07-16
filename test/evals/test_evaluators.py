from typing import Any

import pytest

from evals.evaluators import TextEvaluator, ToolCallEvaluator


@pytest.fixture
def text_evaluator() -> TextEvaluator:
    return TextEvaluator()


@pytest.fixture
def tool_call_evaluator() -> ToolCallEvaluator:
    return ToolCallEvaluator()


def get_turn_payload(query: str, expected: str | list[str], expected_key: str) -> dict[str, Any]:
    return {
        "query": query,
        expected_key: expected,
    }

def get_response_payload(content: str, tool_calls: list[str]) -> dict[str, Any]:
    return {
        "content": content,
        "tool_calls": tool_calls,
    }

@pytest.mark.parametrize(
    "query, expected_text, agent_content, agent_tool_calls, text_coverage",
    [
        ("", [], "", [], 100.0),
        ("who are you", "bosworth", "I'm bosworth", [], 100.0),
        ("who are you", "bosworth", "I'm bosworth", ["dummy_tool"], 100.0),
        ("who are you", "bosworth", "I'm some generic AI agent", [], 0.0),
        ("who are you", "bosworth", "I'm some generic AI agent", [], 0.0),
        ("who are you", ["bosworth", "ai agent"], "I'm Bosworth, an AI agent named after BOS!", [], 100.0),
        ("who are you", ["bosworth", "ai agent"], "I'm an AI agent", [], 50.0),
    ]
)
def test_text_evaluator(query: str, expected_text: str | list[str], agent_content: str, agent_tool_calls: [], text_coverage: float, text_evaluator: TextEvaluator) -> None:
    text_evaluator.evaluate(
        turn=get_turn_payload(query=query, expected=expected_text, expected_key="expected_text"),
        response=get_response_payload(content=agent_content, tool_calls=agent_tool_calls)
    )
    metrics = text_evaluator.metrics()

    assert "text_coverage" in metrics
    assert metrics["text_coverage"] == text_coverage


@pytest.mark.parametrize(
    "query, expected_tool_calls, agent_tool_calls, tool_call_coverage",
    [
        ("", [], [], 100.0),
        ("what's your favorite number", [], [], 100.0),
        ("what's your favorite number", ["get_favorite_number"], ["get_favorite_number"], 100.0),
        ("what's your favorite number", ["get_favorite_number"], [], 0.0),
        ("what's your favorite number", ["get_favorite_number"], ["some_other_tool"], 0.0),
        ("what's your favorite number", ["get_favorite_number", "log_query"], ["get_favorite_number"], 0.0),
        ("what's your favorite number", ["get_favorite_number", "log_query"], ["get_favorite_number", "log_query"], 100.0),
    ]
)
def test_tool_call_evaluator(
    query: str,
    expected_tool_calls: list[str],
    agent_tool_calls: list[str],
    tool_call_coverage: float,
    tool_call_evaluator: ToolCallEvaluator
) -> None:
    turn = get_turn_payload(query=query, expected=expected_tool_calls, expected_key="expected_tool_calls")
    response = get_response_payload(content="some response", tool_calls=agent_tool_calls)

    tool_call_evaluator.evaluate(turn=turn, response=response)
    metrics = tool_call_evaluator.metrics()

    assert "tool_call_coverage" in metrics
    assert metrics["tool_call_coverage"] == tool_call_coverage
