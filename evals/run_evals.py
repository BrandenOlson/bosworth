import json
from functools import lru_cache

import typer
from fastapi.testclient import TestClient
from pathlib import Path

from evals.runner import EvalPipeline
from paths import EVAL_EXAMPLES_FILE
from bosworth.app import app

app_cli = typer.Typer()


@lru_cache
def bosworth_client() -> TestClient:
    return TestClient(app)


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

    pipeline = EvalPipeline(examples, bosworth_client())
    pipeline.run()

    with open(results_path, "w") as f:
        json.dump(pipeline.results(), f, indent=4)

    summary = pipeline.summary()
    print(f"✅ Results written to: {results_path}")
    print(f"📝 Text coverage: {summary['text_coverage']}")
    print(f"🛠️ Tool call coverage: {summary['tool_call_coverage']}")


if __name__ == "__main__":
    app_cli()