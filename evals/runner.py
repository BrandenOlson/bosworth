from copy import deepcopy

from starlette.testclient import TestClient

from evals.evaluators import Turn, BaseEvaluator, TextEvaluator, ToolCallEvaluator


class EvalPipeline:
    def __init__(self, examples: list[list[Turn]], bosworth_client: TestClient):
        self.examples = deepcopy(examples)
        self.bosworth_client = bosworth_client

        self.evaluators: list[BaseEvaluator] = [
            TextEvaluator(),
            ToolCallEvaluator(),
        ]

    def run(self) -> None:
        for example in self.examples:
            for turn in example:
                self.process_turn(turn)

    def process_turn(self, turn: Turn) -> None:
        response = self.bosworth_client.post("/chat", json={"query": turn["query"]})
        for evaluator in self.evaluators:
            evaluator.evaluate(turn, response.json())

    def summary(self) -> dict[str, float]:
        combined = {}
        for evaluator in self.evaluators:
            combined.update(evaluator.metrics())
        return combined

    def results(self) -> list[list[Turn]]:
        return self.examples
