import json
from copy import deepcopy
from functools import lru_cache
from typing import Any

import numpy as np
from fastapi.testclient import TestClient
from starlette.responses import Response

from paths import EVAL_EXAMPLES_FILE
from bosworth.app import app

Turn = dict[str, Any]

@lru_cache
def bosworth_client() -> TestClient:
    return TestClient(app)


with open(EVAL_EXAMPLES_FILE, "r") as f:
    EXAMPLES = json.load(f)


def listify(expected_text: str | list) -> list:
    return expected_text if isinstance(expected_text, list) else [expected_text]

def normalize_text(text: str) -> str:
    return text.lower().strip()


def calculate_text_coverage(actual: str, expected: str | list) -> list[float]:
    actual_text = normalize_text(actual)
    expected_texts = [t.lower() for t in listify(expected)]

    return [100*int(expected in actual_text) for expected in expected_texts]


def calculate_tool_call_coverage(actual: list[str], expected: list[str]) -> list[float]:
    # TODO: generalize to beyond exact match

    return [100*int(actual == expected)]


def evaluate_text(turn: Turn, response: Response) -> None:
    response_text = response.json()["content"]
    turn["agent_response"] = response_text
    if "expected_text" in turn:
        example_expected_text_scores = calculate_text_coverage(normalize_text(response_text), turn["expected_text"])
        expected_text_hits.extend(example_expected_text_scores)

        turn["includes_expected_text"] = example_expected_text_scores

def evaluate_tool_calls(turn: Turn, response: Response) -> None:
    response_tool_calls = response.json()["tool_calls"]
    turn["agent_tool_calls"] = response_tool_calls
    if "expected_tool_calls" in turn:
        example_expected_tool_call_scores = calculate_tool_call_coverage(response_tool_calls, turn["expected_tool_calls"])
        expected_tool_call_hits.extend(example_expected_tool_call_scores)

        turn["includes_expected_tool_calls"] = example_expected_tool_call_scores


def process_turn(turn: dict[str, Any]) -> None:
    response = bosworth_client().post("/chat", json={"query": turn["query"]})

    evaluate_text(turn, response)
    evaluate_tool_calls(turn, response)


if __name__ == "__main__":
    expected_text_hits: list[float] = []
    expected_tool_call_hits: list[float] = []

    examples_with_metrics = deepcopy(EXAMPLES)

    for example in examples_with_metrics:
        for turn in example:
            process_turn(turn)


    RESULTS_FILENAME = "eval_results.json"
    with open(RESULTS_FILENAME, "w") as f:
        json.dump(examples_with_metrics, f, indent=4)

    print(f"Text coverage: {round(np.mean(expected_text_hits), 2)}")
    print(f"Tool call coverage: {round(np.mean(expected_tool_call_hits), 2)}")
