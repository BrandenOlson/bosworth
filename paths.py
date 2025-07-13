from pathlib import Path


BOSWORTH_PATH = Path(__file__).parent

EVALS_PATH = BOSWORTH_PATH / "evals"
EVALS_DATA_PATH = EVALS_PATH / "data"
EVAL_EXAMPLES_FILE = EVALS_DATA_PATH / "examples.json"