import json
from copy import deepcopy
from functools import lru_cache

import numpy as np
from fastapi.testclient import TestClient

from paths import EVAL_EXAMPLES_FILE
from bosworth.app import app

@lru_cache
def bosworth_client() -> TestClient:
    return TestClient(app)


with open(EVAL_EXAMPLES_FILE, "r") as f:
    EXAMPLES = json.load(f)


def listify(expected_text: str | list) -> list:
    return expected_text if isinstance(expected_text, list) else [expected_text]

def normalize_text(text: str) -> str:
    return text.lower().strip()


def evaluate_text(actual: str, expected: str | list) -> list[float]:
    actual_text = normalize_text(actual)
    expected_texts = [t.lower() for t in listify(expected)]

    return [100*int(expected in actual_text) for expected in expected_texts]



def evaluate_tool_calls(actual: list[str], expected: list[str]) -> float:
    # TODO: generalize to beyond exact match

    return 100*int(actual == expected)

expected_text_hits = []
expected_tool_call_hits = []

examples_with_metrics = deepcopy(EXAMPLES)

for example in examples_with_metrics:
    for turn in example:
        response = bosworth_client().post("/chat", json={"query": turn["query"]})
        response_text = response.json()["content"]
        turn["agent_response"] = response_text

        if "expected_text" in turn:
            example_expected_text_scores = evaluate_text(normalize_text(response_text), turn["expected_text"])
            expected_text_hits.extend(example_expected_text_scores)

            turn["includes_expected_text"] = example_expected_text_scores

        response_tool_calls = response.json()["tool_calls"]
        turn["agent_tool_calls"] = response_tool_calls
        if "expected_tool_calls" in turn:
            example_expected_tool_call_score = evaluate_tool_calls(response_tool_calls, turn["expected_tool_calls"])
            expected_tool_call_hits.append(example_expected_tool_call_score)

            turn["includes_expected_tool_calls"] = example_expected_tool_call_score

RESULTS_FILENAME = "eval_results.json"
with open(RESULTS_FILENAME, "w") as f:
    json.dump(examples_with_metrics, f, indent=4)

print(f"Text coverage: {round(np.mean(expected_text_hits), 2)}")
print(f"Tool call coverage: {round(np.mean(expected_tool_call_hits), 2)}")

