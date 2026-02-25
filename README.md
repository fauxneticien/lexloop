# Lexloop

Iterative correction tool for data written in a domain-specific language (DSL). Pick a text file, click Run, see validation results and parsed views in the browser. Edit the file, click Run again — the browser auto-refreshes.

## Setup

Requires Python 3.9+. Uses [uv](https://docs.astral.sh/uv/) for environment management.

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

uv pip install -r requirements.txt
```

## Run (development)

```bash
python app.py
```

1. Click **Browse...** and select your DSL text file.
2. Click **Run**. A browser tab opens with the dashboard at `http://127.0.0.1:8000`.
3. Edit your text file, click **Run** again — the browser reloads automatically.

## Build (standalone executable)

```bash
uv pip install pyinstaller
pyinstaller lexloop.spec
```

The executable is written to `dist/lexloop`. It bundles the `tests/` and `views/` directories.

## Adding tests

Create a `.py` file in `tests/` with a `run` function:

```python
# tests/my_check.py
def run(parsed_data):
    return {
        "name": "My check",
        "passed": True,          # or False
        "details": "Explanation of the result.",
    }
```

## Adding views

Create a `.py` file in `views/` with a `render` function:

```python
# views/my_view.py
def render(parsed_data):
    return {
        "name": "My view",
        "html": "<p>Some HTML here.</p>",
    }
```

## Swapping the parser

Edit `parser.py`. The only requirement is a `parse(file_path)` function that returns a `dict`. Tests and views receive whatever dict you return.

## Project structure

```
app.py          GUI entry point (PyQt6)
runner.py       Orchestration: parse → test → view → HTML → serve
parser.py       DSL parser (stub — replace with yours)
server.py       Background HTTP server
templates.py    HTML templates and auto-refresh JS
lexloop.spec    PyInstaller build spec
tests/          Validation test modules (drop .py files here)
views/          View modules (drop .py files here)
output/         Generated HTML (gitignored, created at runtime)
```
