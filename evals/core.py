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
