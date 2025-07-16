import pytest

from evals.evaluators import TextEvaluator, ToolCallEvaluator


@pytest.fixture
def text_evaluator() -> TextEvaluator:
    return TextEvaluator()


@pytest.fixture
def tool_call_evaluator() -> ToolCallEvaluator:
    return ToolCallEvaluator()


def test_text_evaluator(text_evaluator: TextEvaluator) -> None:
    turn = {
      "query": "who are you",
      "expected_text": ["bosworth"]
    }
    response = {
            "content": "I'm Bosworth!",
            "tool_calls": [],
        }
    text_evaluator.evaluate(turn=turn, response=response)
    metrics = text_evaluator.metrics()

    assert "text_coverage" in metrics
    assert metrics["text_coverage"] == 100.0


def test_tool_call_evaluator(tool_call_evaluator: ToolCallEvaluator) -> None:
    turn = {
        "query": "what's your favorite number",
        "expected_tool_calls": ["get_favorite_number"]
    }
    response = {
        "content": "My favorite number is 13",
        "tool_calls": ["get_favorite_number"],
    }
    tool_call_evaluator.evaluate(turn=turn, response=response)
    metrics = tool_call_evaluator.metrics()

    assert "tool_call_coverage" in metrics
    assert metrics["tool_call_coverage"] == 100.0
