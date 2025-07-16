from typing import Any, Callable
import numpy as np

from starlette.responses import Response

from evals.core import calculate_text_coverage, calculate_tool_call_coverage


Turn = dict[str, Any]


class BaseEvaluator:
    def evaluate(self, turn: Turn, response: dict[str, Any]) -> None:
        raise NotImplementedError

    def metrics(self) -> dict[str, float]:
        raise NotImplementedError


class ScoringEvaluator(BaseEvaluator):
    def __init__(
        self,
        *,
        response_key: str,
        expected_key: str,
        turn_output_key: str,
        scoring_fn: Callable[[Any, Any], list[bool]],
        result_key: str,
    ):
        self.response_key = response_key
        self.expected_key = expected_key
        self.turn_output_key = turn_output_key
        self.scoring_fn = scoring_fn
        self.result_key = result_key
        self._hits: list[float] = []

    def evaluate(self, turn: Turn, response: dict[str, Any]) -> None:
        actual = response[self.response_key]
        turn[f"agent_{self.response_key}"] = actual

        if self.expected_key in turn:
            expected = turn[self.expected_key]
            scores = self.scoring_fn(actual, expected)
            turn[self.turn_output_key] = scores
            self._hits.extend(scores)



    def metrics(self) -> dict[str, float]:
        return {
            self.result_key: float(round(100.0*np.mean(self._hits), 2) if self._hits else 100.0)
        }


class TextEvaluator(ScoringEvaluator):
    def __init__(self) -> None:
        super().__init__(
            response_key="content",
            expected_key="expected_text",
            turn_output_key="includes_expected_text",
            scoring_fn=calculate_text_coverage,
            result_key="text_coverage",
        )


class ToolCallEvaluator(ScoringEvaluator):
    def __init__(self) -> None:
        super().__init__(
            response_key="tool_calls",
            expected_key="expected_tool_calls",
            turn_output_key="includes_expected_tool_calls",
            scoring_fn=calculate_tool_call_coverage,
            result_key="tool_call_coverage",
        )
