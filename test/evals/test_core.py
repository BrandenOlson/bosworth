import pytest

from evals.core import listify, normalize_text, calculate_tool_call_coverage, calculate_text_coverage

@pytest.mark.parametrize(
    "example_input, expected_output",
    [
        ("", [""]),
        ([], []),
        ("blah", ["blah"]),
        (["blah blah"], ["blah blah"]),
        (["foo", "bar"], ["foo", "bar"]),
    ]
)
def test_listify(example_input: str | list[str], expected_output: list[str]) -> None:
    assert listify(example_input) == expected_output

@pytest.mark.parametrize(
    "example_input, expected_output",
    [
        ("", ""),
        ("bos life", "bos life"),
        ("BOS Life", "bos life"),
        ("  bosworth  ", "bosworth"),
        ("\nHello, I'm Bosworth!\n", "hello, i'm bosworth!")
    ]
)
def test_normalize_text(example_input: str, expected_output: str) -> None:
    assert normalize_text(example_input) == expected_output


@pytest.mark.parametrize(
    "actual, expected, expected_coverage",
    [
        ("i'm bosworth, an ai agent", ["bosworth", "ai agent"], [True, True]),
        ("wentworth", ["bos", "worth"], [False, True]),
        ("unrelated text", "reference text", [False]),
    ]
)
def test_calculate_text_coverage(actual: str, expected: list[str], expected_coverage: float):
    assert calculate_text_coverage(actual, expected) == expected_coverage


@pytest.mark.parametrize(
    "actual, expected, expected_coverage",
    [
        ([], [], [True]),
        ([], ["dummy_tool"], [False]),
        (["dummy_tool"], [], [False]),
        (["dummy_tool"], ["dummy_tool"], [True]),
        (["tool_1", "tool_2"], ["tool_1", "tool_2"], [True]),
        (["tool_1", "tool_2"], ["tool_1"], [False]),
        (["tool_1", "tool_2"], ["tool_2"], [False]),
        (["tool_1", "tool_2"], ["tool_1", "tool_3"], [False]),
        (["tool_1", "tool_2"], ["tool_3", "tool_4"], [False]),
    ]
)
def test_calculate_tool_call_coverage(actual: list[str], expected: list[str], expected_coverage: float):
    assert calculate_tool_call_coverage(actual, expected) == expected_coverage
