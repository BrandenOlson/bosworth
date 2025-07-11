# bosworth
A BOS agent worth your while


## Setup 

(Tested with Python 3.12.7.
For best results, make sure your `python3` has this version.
You can use [`pyenv`](https://github.com/pyenv/pyenv) for local `python` versioning if needed.)



Create + activate Python env:

```
python3 -m venv ~/envs/bosworth
source ~/envs/bosworth/bin/activate
```

TODO: Set up packages via `uv`

Start app in a shell:
```
PYTHONPATH=. python bosworth/app/main.py
```


```
> curl localhost:8000/chat -X POST -H 'Content-Type: application/json' -d '{"query": "hello"}' && echo

{"content":"Hello! It's great to meet you! I'm Bosworth, your friendly finance AI agent. I'm here to help answer any questions you have about personal finance, investing, or anything else related to money management.\n\nWhat can I assist you with today? Do you have a specific question or topic in mind?"}
```

Run the tests via
```
pytest test
```

Run type checking via
```
mypy .
```