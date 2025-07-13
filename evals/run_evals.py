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


expected_text_hits = []

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

RESULTS_FILENAME = "eval_results.json"
with open(RESULTS_FILENAME, "w") as f:
    json.dump(examples_with_metrics, f, indent=4)

print(round(np.mean(expected_text_hits), 2))

