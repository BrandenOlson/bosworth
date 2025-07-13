import json
from copy import deepcopy
from functools import lru_cache
from typing import Any

import numpy as np
import typer
from fastapi.testclient import TestClient
from pathlib import Path
from starlette.responses import Response

from paths import EVAL_EXAMPLES_FILE
from bosworth.app import app

app_cli = typer.Typer()
Turn = dict[str, Any]


@lru_cache
def bosworth_client() -> TestClient:
    return TestClient(app)


def listify(expected_text: str | list) -> list:
    return expected_text if isinstance(expected_text, list) else [expected_text]


def normalize_text(text: str) -> str:
    return text.lower().strip()


def calculate_text_coverage(actual: str, expected: str | list) -> list[float]:
    actual_text = normalize_text(actual)
    expected_texts = [t.lower() for t in listify(expected)]
    return [100 * int(expected in actual_text) for expected in expected_texts]


def calculate_tool_call_coverage(actual: list[str], expected: list[str]) -> list[float]:
    # TODO: generalize to beyond exact match
    return [100 * int(actual == expected)]


class Evaluator:
    def __init__(self, examples: list[list[Turn]]):
        self.examples = deepcopy(examples)
        self.expected_text_hits: list[float] = []
        self.expected_tool_call_hits: list[float] = []

    def run(self) -> None:
        for example in self.examples:
            for turn in example:
                self.process_turn(turn)

    def process_turn(self, turn: Turn) -> None:
        response = bosworth_client().post("/chat", json={"query": turn["query"]})
        self.evaluate_text(turn, response)
        self.evaluate_tool_calls(turn, response)

    def evaluate_text(self, turn: Turn, response: Response) -> None:
        response_text = response.json()["content"]
        turn["agent_response"] = response_text

        if "expected_text" in turn:
            scores = calculate_text_coverage(response_text, turn["expected_text"])
            turn["includes_expected_text"] = scores
            self.expected_text_hits.extend(scores)

    def evaluate_tool_calls(self, turn: Turn, response: Response) -> None:
        tool_calls = response.json()["tool_calls"]
        turn["agent_tool_calls"] = tool_calls

        if "expected_tool_calls" in turn:
            scores = calculate_tool_call_coverage(tool_calls, turn["expected_tool_calls"])
            turn["includes_expected_tool_calls"] = scores
            self.expected_tool_call_hits.extend(scores)

    def summary(self) -> dict[str, float]:
        return {
            "text_coverage": float(round(np.mean(self.expected_text_hits), 2) if self.expected_text_hits else 0.0),
            "tool_call_coverage": float(round(np.mean(self.expected_tool_call_hits), 2) if self.expected_tool_call_hits else 0.0),
        }

    def results(self) -> list[list[Turn]]:
        return self.examples


@app_cli.command()
def main(
    outdir: Path = typer.Option(
        ..., "--outdir", "-o",
        help="Directory where eval results will be saved",
        exists=False, file_okay=False, writable=True, resolve_path=True,
    )
) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    results_path = outdir / "metrics.json"

    with open(EVAL_EXAMPLES_FILE, "r") as f:
        examples = json.load(f)

    evaluator = Evaluator(examples)
    evaluator.run()

    with open(results_path, "w") as f:
        json.dump(evaluator.results(), f, indent=4)

    summary = evaluator.summary()
    print(f"✅ Results written to: {results_path}")
    print(f"📝 Text coverage: {summary['text_coverage']}")
    print(f"🛠️ Tool call coverage: {summary['tool_call_coverage']}")


if __name__ == "__main__":
    app_cli()