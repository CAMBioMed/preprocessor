# Benthic Image Preprocessor

[Annotation Guide](https://cambiomed-biodiversa.com/guide/)

## Installation
Download the latest nightly (unstable) release:

1.  Go to the latest [Package workflow run](https://github.com/CAMBioMed/preprocessor/actions/workflows/package.yaml).
2.  Download the appropriate artifact for your system, one of:

    - Windows (`cambiomed-preprocessor-Windows.zip`)
    - MacOS (`cambiomed-preprocessor-macOS.zip`)
    - Ubuntu (`cambiomed-preprocessor-Ubuntu-24.04.zip`)
    - Fedora (`cambiomed-preprocessor-Fedora-40.zip`)


## Developer tasks
- Sync dependencies: `uv sync` (`make sync`)
- Run CLI: `uv run preprocessor` (`make run`)
- Run GUI: `uv run preprocessor gui` (`make run-gui`)
- Run tests: `uv run pytest -q` (`make test`)
- Run tests with coverage: `uv run pytest -q --cov` (`make test-coverage`)
- Determine version: `uv run hatch version` (`make version`)
- Lint code: `uv run ruff check .` (`make lint`)
- Format code: `uv run ruff format .` (`make format`)
- Build app and UI files: `uv run pyside6-project build` and `uv build` (`make build`)
- Mypy type checking: `uv run mypy src tests` (`make typecheck`)
- Run briefcase app with app update and updating dependencies: `uvx briefcase run -u -r` (`make app-run`)

