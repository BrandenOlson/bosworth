# bosworth 
### A boss agent worth your while 🦾💰

![Python](https://img.shields.io/badge/python-3.12-blue)
![LangGraph](https://img.shields.io/badge/langgraph-🧠-purple)
![FastAPI](https://img.shields.io/badge/framework-fastapi-009688)
![License](https://img.shields.io/github/license/BrandenOlson/bosworth)

#### Disclaimer: This project is very much a work-in-progress. Please reach out with any questions!


## Overview

`bosworth` is a simple agentic chatbot powered by [`ollama`](https://ollama.com), [`langgraph`](https://www.langchain.com/langgraph), and [`fastapi`](https://fastapi.tiangolo.com).
It remembers things, calls tools, and runs with a single `curl` (though a CLI / GUI are on the horizon!).


## Setup 

First make sure `ollama` is installed and able to serve required models:
```commandline
./setup.sh
```

(Tested with Python 3.12.7.
For best results, make sure your `python3` has this version.
You can use [`pyenv`](https://github.com/pyenv/pyenv) for local `python` versioning if needed.)



Create + activate Python env:

```commandline
python3 -m venv ~/envs/bosworth
source ~/envs/bosworth/bin/activate
```

- TODO: Combine python evn setup into `setup.sh`
- TODO: Set up packages via `uv`


## Runtime

Start app in a shell:
```commandline
PYTHONPATH=. python bosworth/app/main.py
```


```commandline
curl localhost:8000/chat -X POST -H 'Content-Type: application/json' -d '{"query": "hello"}' && echo

{"content":"Hello! It's great to meet you! I'm Bosworth, your friendly finance AI agent. I'm here to help answer any questions you have about personal finance, investing, or anything else related to money management.\n\nWhat can I assist you with today? Do you have a specific question or topic in mind?"}
```

## Checks

Run the tests via
```commandline
pytest test
```

Run type checking via
```commandline
mypy .
```

Run evals via
```commandline
PYTHONPATH=. python evals/run_evals.py
```
