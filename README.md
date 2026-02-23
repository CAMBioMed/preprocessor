# Benthic Image Preprocessor

[Annotation Guide](https://cambiomed-biodiversa.com/guide/)

## Everyday tasks
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
- Run briefcase app with app update and updating dependencies: `uvx briefcase run -u -r`

## Create UI files
To create or update the generated Python UI files, use the following command:

```shell
uv run pyside6-project build
```

> [!NOTE]
> I tried adding the [hatch-pyside](https://github.com/s-ball/hatch-pyside) plugin to Hatch to make this step automatic, but the plugin does not support PySide6 > 6.8 and doesn't understand the `pyproject.toml` file.

